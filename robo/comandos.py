"""A lista fechada do que o robô entende e a regra que separa comando de conversa.

O robô ouve a conversa inteira do Flávio com a Luna. Só é comando a frase que
é, do começo ao fim, o nome do robô seguido de uma frase desta lista; qualquer
outra coisa é conversa e o robô ignora (decisões D2 e D5 do plano).
"""
from dataclasses import dataclass

NOME_DO_ROBO = "python"

PALAVRA_DESCONHECIDA = "[unk]"

# "Chrome" não existe no vocabulário do modelo de voz; "cromo" soa igual.
FRASES_DOS_COMANDOS = {
    "abre o cromo": "abrir_chrome",
}


@dataclass(frozen=True)
class Comando:
    nome: str
    frase_ouvida: str


def montar_lista_fechada():
    """As únicas frases que o reconhecedor pode devolver; o resto vira [unk]."""
    frases = [f"{NOME_DO_ROBO} {frase}" for frase in FRASES_DOS_COMANDOS]
    return frases + [PALAVRA_DESCONHECIDA]


def interpretar_frase(frase_ouvida):
    """Devolve o Comando da frase, ou None quando a frase é conversa."""
    palavras = frase_ouvida.split()
    if not palavras or palavras[0] != NOME_DO_ROBO:
        return None
    pedido = " ".join(palavras[1:])
    nome_do_comando = FRASES_DOS_COMANDOS.get(pedido)
    if nome_do_comando is None:
        return None
    return Comando(nome_do_comando, frase_ouvida)
