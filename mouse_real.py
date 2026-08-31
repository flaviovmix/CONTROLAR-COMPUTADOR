"""Mouse "de verdade" via SendInput + ativacao de janela.

pyautogui e pynput movem o cursor com SetCursorPos, que so teleporta o
ponteiro sem gerar evento de entrada. Apps WinUI (Paint novo etc.) ignoram
esse teleporte com o botao apertado, entao o arrasto nao funciona.
SendInput injeta o movimento na fila de entrada do Windows como mouse fisico.

Validado em 29/08/2026 desenhando no Paint (ver .claude/commands/controlando-teclado-mouse.md).
"""

import ctypes
import time
from ctypes import wintypes

import pyautogui
import pygetwindow

MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_ABSOLUTE = 0x8000
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP = 0x0040
MOUSEEVENTF_WHEEL = 0x0800
INPUT_MOUSE = 0

APERTA_E_SOLTA = {
    "esquerdo": (MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP),
    "direito": (MOUSEEVENTF_RIGHTDOWN, MOUSEEVENTF_RIGHTUP),
    "meio": (MOUSEEVENTF_MIDDLEDOWN, MOUSEEVENTF_MIDDLEUP),
}

PASSO_EM_PIXELS = 3
PAUSA_ENTRE_PASSOS = 0.002


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(wintypes.ULONG)),
    ]


class INPUT(ctypes.Structure):
    _fields_ = [("type", wintypes.DWORD), ("mi", MOUSEINPUT)]


def enviar_evento_de_mouse(flags, dx=0, dy=0, dados=0):
    evento = INPUT(type=INPUT_MOUSE, mi=MOUSEINPUT(dx=dx, dy=dy, mouseData=dados, dwFlags=flags))
    ctypes.windll.user32.SendInput(1, ctypes.byref(evento), ctypes.sizeof(evento))


def mover_para(x, y):
    """Coordenada absoluta normalizada em 0..65535, como o Windows exige."""
    largura, altura = pyautogui.size()
    dx = round(x * 65535 / (largura - 1))
    dy = round(y * 65535 / (altura - 1))
    enviar_evento_de_mouse(MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE, dx, dy)


def apertar(botao="esquerdo"):
    enviar_evento_de_mouse(APERTA_E_SOLTA[botao][0])


def soltar(botao="esquerdo"):
    enviar_evento_de_mouse(APERTA_E_SOLTA[botao][1])


def clicar(x, y, botao="esquerdo"):
    mover_para(x, y)
    time.sleep(0.05)
    apertar(botao)
    time.sleep(0.03)
    soltar(botao)


def deslizar_ate(origem, destino):
    """Anda em passinhos pra o app registrar o arrasto, nao um teleporte."""
    origem_x, origem_y = origem
    destino_x, destino_y = destino
    distancia = max(abs(destino_x - origem_x), abs(destino_y - origem_y))
    passos = max(1, distancia // PASSO_EM_PIXELS)
    for i in range(1, passos + 1):
        fracao = i / passos
        mover_para(
            round(origem_x + (destino_x - origem_x) * fracao),
            round(origem_y + (destino_y - origem_y) * fracao),
        )
        time.sleep(PAUSA_ENTRE_PASSOS)


def arrastar(origem, destino, botao="esquerdo"):
    mover_para(*origem)
    time.sleep(0.1)
    apertar(botao)
    deslizar_ate(origem, destino)
    soltar(botao)


def rolar(cliques_de_roda, x=None, y=None):
    """Positivo rola pra cima. 1 clique de roda = 120 no Windows."""
    if x is not None:
        mover_para(x, y)
        time.sleep(0.05)
    enviar_evento_de_mouse(MOUSEEVENTF_WHEEL, dados=ctypes.c_ulong(cliques_de_roda * 120).value)


def ativar_janela(titulo):
    """Traz pra frente a janela com esse titulo exato. Devolve True se conseguiu.

    O toque no Alt e o truque que faz o Windows liberar a troca de foco
    pra um processo em segundo plano.
    """
    candidatas = [j for j in pygetwindow.getAllWindows() if j.title == titulo]
    if not candidatas:
        return False
    janela = candidatas[0]
    pyautogui.press("alt")
    try:
        janela.activate()
    except Exception:
        return False
    time.sleep(0.5)
    ativa = pygetwindow.getActiveWindow()
    return ativa is not None and ativa.title == titulo
