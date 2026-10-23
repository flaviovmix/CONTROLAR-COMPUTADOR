"""O ouvido com áudio de verdade: cada voz gravada em audios/<voz>/comando e audios/<voz>/conversa.

A voz Maria (a do Windows) vem no git. A voz do Flávio fica só na máquina dele
(audios/flavio/, fora do git) e entra sozinha aqui quando existir.
"""
import wave
from pathlib import Path

import pytest

from robo.comandos import interpretar_frase
from robo.ouvido import PASTA_DO_MODELO, carregar_modelo, ouvir_arquivo

PASTA_DOS_AUDIOS = Path(__file__).parent / "audios"

pytestmark = pytest.mark.skipif(
    not PASTA_DO_MODELO.is_dir(), reason="modelo de voz não baixado (ver LEIA-ME)"
)


def listar_audios(tipo):
    return sorted(PASTA_DOS_AUDIOS.glob(f"*/{tipo}/*.wav"))


def nome_do_audio(caminho):
    return f"{caminho.parent.parent.name}/{caminho.stem}"


@pytest.fixture(scope="module")
def modelo():
    return carregar_modelo()


def comandos_ouvidos(modelo, caminho_do_wav):
    frases = ouvir_arquivo(modelo, caminho_do_wav)
    return frases, [comando for comando in map(interpretar_frase, frases) if comando]


@pytest.mark.parametrize("caminho_do_wav", listar_audios("comando"), ids=nome_do_audio)
def test_comando_falado_vira_um_comando(modelo, caminho_do_wav):
    frases, comandos = comandos_ouvidos(modelo, caminho_do_wav)
    assert [comando.nome for comando in comandos] == ["abrir_chrome"], f"ouviu {frases}"


@pytest.mark.parametrize("caminho_do_wav", listar_audios("conversa"), ids=nome_do_audio)
def test_conversa_falada_nao_vira_comando(modelo, caminho_do_wav):
    frases, comandos = comandos_ouvidos(modelo, caminho_do_wav)
    assert comandos == [], f"ouviu {frases}"


def test_audio_estereo_e_recusado(modelo, tmp_path):
    caminho_do_wav = tmp_path / "estereo.wav"
    with wave.open(str(caminho_do_wav), "wb") as audio:
        audio.setnchannels(2)
        audio.setsampwidth(2)
        audio.setframerate(16000)
        audio.writeframes(b"\x00\x00" * 2 * 1600)
    with pytest.raises(ValueError, match="mono"):
        ouvir_arquivo(modelo, caminho_do_wav)
