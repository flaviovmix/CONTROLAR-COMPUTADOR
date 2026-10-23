"""O ouvido do robô: o microfone, ou um arquivo de áudio, passando pelo reconhecedor.

O reconhecedor é o Vosk com o modelo pequeno de português, que roda sem
internet e sem placa de vídeo. Ele só devolve frases da lista fechada de
robo.comandos; o resto da conversa chega como [unk].

O microfone é aberto em modo compartilhado (o padrão do Windows), então a
conversa com a Luna no navegador continua ouvindo o mesmo microfone.
"""
import json
import queue
import wave
from pathlib import Path

import sounddevice
from vosk import KaldiRecognizer, Model, SetLogLevel

from robo.comandos import montar_lista_fechada

TAXA_DE_AMOSTRAGEM = 16000
AMOSTRAS_POR_BLOCO = 4000  # um quarto de segundo
PASTA_DO_MODELO = Path(__file__).parent / "modelos" / "vosk-model-small-pt-0.3"


def carregar_modelo(pasta_do_modelo=PASTA_DO_MODELO):
    if not Path(pasta_do_modelo).is_dir():
        raise FileNotFoundError(
            f"Modelo de voz não encontrado em {pasta_do_modelo}. O LEIA-ME ensina a baixar."
        )
    SetLogLevel(-1)
    return Model(str(pasta_do_modelo))


def criar_reconhecedor(modelo, taxa_de_amostragem=TAXA_DE_AMOSTRAGEM):
    return KaldiRecognizer(modelo, taxa_de_amostragem, json.dumps(montar_lista_fechada()))


def ler_texto(resultado_do_reconhecedor):
    return json.loads(resultado_do_reconhecedor).get("text", "")


def listar_microfones():
    """(índice, nome) dos microfones do sistema de som padrão do Windows (o MME).

    O MME corta o nome em 31 letras, mas converte o som pra 16 kHz sozinho, que
    é a taxa que o modelo de voz espera.
    """
    sistema_padrao = sounddevice.default.hostapi
    return [
        (indice, aparelho["name"])
        for indice, aparelho in enumerate(sounddevice.query_devices())
        if aparelho["hostapi"] == sistema_padrao and aparelho["max_input_channels"] > 0
    ]


def achar_microfone(pedaco_do_nome):
    """O índice do único microfone cujo nome tem o pedaço dado; sem pedaço, o padrão do Windows.

    Nesta máquina o padrão do Windows é a placa de captura de vídeo, não um
    microfone: por isso o robô deixa escolher pelo nome.
    """
    if not pedaco_do_nome:
        return None
    achados = [
        (indice, nome)
        for indice, nome in listar_microfones()
        if pedaco_do_nome.lower() in nome.lower()
    ]
    if len(achados) != 1:
        nomes = ", ".join(nome for _indice, nome in listar_microfones())
        raise ValueError(
            f"{len(achados)} microfones com '{pedaco_do_nome}' no nome. Os que existem: {nomes}"
        )
    return achados[0][0]


def escutar_microfone(modelo, microfone=None):
    """Entrega cada frase ouvida no microfone, sem parar (Ctrl+C para)."""
    reconhecedor = criar_reconhecedor(modelo)
    blocos_de_audio = queue.Queue()

    def guardar_bloco(dados, _quadros, _tempo, _situacao):
        blocos_de_audio.put(bytes(dados))

    with sounddevice.RawInputStream(
        samplerate=TAXA_DE_AMOSTRAGEM,
        blocksize=AMOSTRAS_POR_BLOCO,
        dtype="int16",
        channels=1,
        device=microfone,
        callback=guardar_bloco,
    ):
        while True:
            if reconhecedor.AcceptWaveform(blocos_de_audio.get()):
                frase = ler_texto(reconhecedor.Result())
                if frase:
                    yield frase


def conferir_formato_do_wav(audio, caminho_do_wav):
    """O reconhecedor espera áudio mono de 16 bits; outro formato vira lixo calado."""
    if audio.getnchannels() != 1 or audio.getsampwidth() != 2:
        raise ValueError(f"{caminho_do_wav}: o áudio precisa ser mono e de 16 bits.")


def ouvir_arquivo(modelo, caminho_do_wav):
    """As frases de um .wav, pelo mesmo reconhecedor do microfone. Usado nas provas."""
    frases = []
    with wave.open(str(caminho_do_wav), "rb") as audio:
        conferir_formato_do_wav(audio, caminho_do_wav)
        reconhecedor = criar_reconhecedor(modelo, audio.getframerate())
        while bloco := audio.readframes(AMOSTRAS_POR_BLOCO):
            if reconhecedor.AcceptWaveform(bloco):
                frases.append(ler_texto(reconhecedor.Result()))
        frases.append(ler_texto(reconhecedor.FinalResult()))
    return [frase for frase in frases if frase]
