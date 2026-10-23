"""Grava a voz do Flávio pras provas do robô: 10 comandos e 10 frases de conversa.

Uso, na raiz do projeto:
  .venv\\Scripts\\python -m robo.testes.gravar_minha_voz --microfone Realtek
Cada frase aparece na tela. Aperte Enter, fale, e a gravação para sozinha.
Os arquivos vão pra robo/testes/audios/flavio/, que fica fora do git.
"""
import argparse
import wave
from pathlib import Path

import sounddevice

from robo.ouvido import achar_microfone

TAXA_DE_AMOSTRAGEM = 16000
SEGUNDOS_POR_FRASE = 4
PASTA_DA_VOZ = Path(__file__).parent / "audios" / "flavio"

FRASES_DE_COMANDO = ["Python, abre o Chrome."] * 10

FRASES_DE_CONVERSA = [
    "Luna, o que você acha do Python?",
    "Eu programo em Python faz tempo.",
    "Abre o Chrome pra mim depois.",
    "O Python é uma linguagem boa pra começar.",
    "Será que o Python consegue abrir o Chrome sozinho?",
    "Meu pai abre o Chrome todo dia.",
    "Hoje a gente vai testar o robô.",
    "Luna, abre o Chrome.",
    "Python é o nome do robô.",
    "Fala, Luna, tudo bem?",
]


def ler_microfone_escolhido():
    leitor = argparse.ArgumentParser(prog="python -m robo.testes.gravar_minha_voz")
    leitor.add_argument("--microfone", help="um pedaço do nome do microfone (ex.: Realtek)")
    return achar_microfone(leitor.parse_args().microfone)


def gravar_frase(microfone):
    """Os bytes de SEGUNDOS_POR_FRASE de microfone (o fluxo cru dispensa o numpy)."""
    with sounddevice.RawInputStream(
        samplerate=TAXA_DE_AMOSTRAGEM, channels=1, dtype="int16", device=microfone
    ) as fluxo:
        amostras, _transbordou = fluxo.read(SEGUNDOS_POR_FRASE * TAXA_DE_AMOSTRAGEM)
    return bytes(amostras)


def salvar_wav(caminho_do_wav, amostras):
    caminho_do_wav.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(caminho_do_wav), "wb") as audio:
        audio.setnchannels(1)
        audio.setsampwidth(2)
        audio.setframerate(TAXA_DE_AMOSTRAGEM)
        audio.writeframes(amostras)


def gravar_lista(tipo, frases, microfone):
    for numero, frase in enumerate(frases, start=1):
        input(f"\n[{tipo} {numero} de {len(frases)}]  Fale:  {frase}\n  Enter e fale... ")
        print("  gravando...", flush=True)
        salvar_wav(PASTA_DA_VOZ / tipo / f"{numero:02d}.wav", gravar_frase(microfone))
        print("  pronto.", flush=True)


def main():
    microfone = ler_microfone_escolhido()
    print(f"Cada gravação dura {SEGUNDOS_POR_FRASE} segundos. Fale logo depois do Enter.")
    gravar_lista("comando", FRASES_DE_COMANDO, microfone)
    gravar_lista("conversa", FRASES_DE_CONVERSA, microfone)
    print(f"\nTudo gravado em {PASTA_DA_VOZ}. Agora as provas rodam com a sua voz.")


if __name__ == "__main__":
    main()
