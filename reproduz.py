"""Reproduz uma gravacao feita pelo gravador.py.

Uso:  python reproduz.py <nome-da-tarefa> [--seco] [--fiel]

--seco  so lista os passos, sem tocar no mouse (pra conferir antes)
--fiel  respeita as esperas originais entre passos (default: teto de 3s)

Freio de emergencia: mouse no canto superior esquerdo aborta (FAILSAFE).
"""

import json
import sys
import time
from pathlib import Path

import pyautogui
import pyperclip

import mouse_real

pyautogui.FAILSAFE = True

TETO_DE_ESPERA = 3.0  # segundos entre passos, fora do modo --fiel


def carregar(nome):
    caminho = Path(__file__).parent / "gravacoes" / nome / "passos.json"
    if not caminho.exists():
        raise SystemExit(f"Nao achei {caminho}. Grave antes com: python gravador.py {nome}")
    return json.loads(caminho.read_text(encoding="utf-8"))


def descrever(passo):
    detalhe = {k: v for k, v in passo.items() if k not in ("tipo", "espera", "janela", "recorte")}
    return f"{passo['tipo']}: {json.dumps(detalhe, ensure_ascii=False)}"


def garantir_janela(titulo, janela_atual):
    """Best effort: tenta trazer a janela gravada pra frente quando ela muda."""
    if not titulo or titulo == janela_atual:
        return janela_atual
    if not mouse_real.ativar_janela(titulo):
        print(f"  aviso: nao achei a janela '{titulo}'; seguindo com a que estiver na frente")
    return titulo


def digitar(texto):
    """pyautogui.write nao digita acento; texto com acento entra via clipboard."""
    if texto.isascii():
        pyautogui.write(texto, interval=0.03)
    else:
        guardado = pyperclip.paste()
        pyperclip.copy(texto)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.2)
        pyperclip.copy(guardado)


def executar(passo, janela_atual):
    tipo = passo["tipo"]
    if tipo == "clique":
        janela_atual = garantir_janela(passo.get("janela", ""), janela_atual)
        mouse_real.clicar(passo["x"], passo["y"], passo["botao"])
    elif tipo == "arrasto":
        janela_atual = garantir_janela(passo.get("janela", ""), janela_atual)
        mouse_real.arrastar(tuple(passo["de"]), tuple(passo["ate"]), passo["botao"])
    elif tipo == "rolagem":
        mouse_real.rolar(passo["cliques"], passo["x"], passo["y"])
    elif tipo == "digita":
        digitar(passo["texto"])
    elif tipo == "atalho":
        pyautogui.hotkey(*passo["teclas"].split("+"))
    elif tipo == "tecla":
        pyautogui.press(passo["tecla"])
    else:
        print(f"  aviso: tipo desconhecido '{tipo}', pulando")
    return janela_atual


def main():
    argumentos = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not argumentos:
        raise SystemExit("Uso: python reproduz.py <nome-da-tarefa> [--seco] [--fiel]")
    seco = "--seco" in sys.argv
    fiel = "--fiel" in sys.argv

    gravacao = carregar(argumentos[0])
    passos = gravacao["passos"]
    print(f"Tarefa '{gravacao['tarefa']}' ({len(passos)} passos, gravada em {gravacao['gravado_em']})")

    if seco:
        for i, passo in enumerate(passos, 1):
            print(f"  {i:3d}. [{passo.get('espera', 0):5.1f}s] {descrever(passo)}")
        return

    tela_gravada = gravacao.get("tela")
    if tela_gravada and tuple(tela_gravada) != tuple(pyautogui.size()):
        print(f"  aviso: gravado em {tela_gravada}, tela atual {list(pyautogui.size())}; coordenadas podem nao bater")

    print("Comeca em 3 segundos. Pra abortar, jogue o mouse no canto superior esquerdo.")
    time.sleep(3)
    janela_atual = ""
    for i, passo in enumerate(passos, 1):
        espera = passo.get("espera", 0)
        time.sleep(espera if fiel else min(espera, TETO_DE_ESPERA))
        print(f"  {i:3d}. {descrever(passo)}")
        janela_atual = executar(passo, janela_atual)
    print("Fim.")


if __name__ == "__main__":
    main()
