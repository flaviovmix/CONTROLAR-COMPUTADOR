"""A regra que separa comando de conversa, sem microfone nem modelo de voz."""
import pytest

from robo.comandos import Comando, interpretar_frase, montar_lista_fechada


def test_nome_seguido_do_comando_vira_comando():
    assert interpretar_frase("python abre o cromo") == Comando("abrir_chrome", "python abre o cromo")


@pytest.mark.parametrize(
    "frase_ouvida",
    [
        "",
        "python",
        "abre o cromo",  # sem o nome
        "o python",  # o nome no fim de uma pergunta à Luna
        "[unk] python abre o cromo",  # o nome no meio da conversa
        "python abre o cromo [unk]",  # comando com conversa colada depois
        "python [unk]",  # o nome com um pedido que não está na lista
    ],
)
def test_conversa_nao_vira_comando(frase_ouvida):
    assert interpretar_frase(frase_ouvida) is None


def test_lista_fechada_tem_os_comandos_e_a_palavra_desconhecida():
    assert montar_lista_fechada() == ["python abre o cromo", "[unk]"]
