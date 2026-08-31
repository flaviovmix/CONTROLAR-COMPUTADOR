"""Grava uma sequencia de cliques e teclas pra virar automacao depois.

Uso:  python gravador.py <nome-da-tarefa>
Faca a tarefa normalmente e aperte F10 pra encerrar.

Sai em gravacoes/<nome>/: passos.json (a sequencia) + um recorte de tela
por clique (o botao que foi apertado, pra reencontrar depois com
locateOnScreen se ele mudar de lugar).
"""

import json
import sys
import time
from datetime import datetime
from pathlib import Path

import pyautogui
import pygetwindow
from pynput import keyboard, mouse

TECLA_DE_PARADA = keyboard.Key.f10
TAMANHO_DO_RECORTE = 120        # px de lado, centrado no clique
DISTANCIA_MINIMA_DE_ARRASTO = 5 # px; menos que isso e clique

MODIFICADORES = {
    keyboard.Key.ctrl_l: "ctrl", keyboard.Key.ctrl_r: "ctrl",
    keyboard.Key.alt_l: "alt", keyboard.Key.alt_r: "alt", keyboard.Key.alt_gr: "altgr",
    keyboard.Key.cmd: "win",
    keyboard.Key.shift: "shift", keyboard.Key.shift_r: "shift",
}

NOME_DO_BOTAO = {"left": "esquerdo", "right": "direito", "middle": "meio"}


class Gravador:
    def __init__(self, pasta):
        self.pasta = pasta
        self.passos = []
        self.texto_corrente = ""
        self.ultimo_tempo = time.time()
        self.modificadores_apertados = set()
        self.inicio_do_arrasto = None

    # --- utilitarios -----------------------------------------------------

    def espera_desde_o_passo_anterior(self):
        agora = time.time()
        delta = round(agora - self.ultimo_tempo, 2)
        self.ultimo_tempo = agora
        return delta

    def titulo_da_janela_ativa(self):
        janela = pygetwindow.getActiveWindow()
        return janela.title if janela else ""

    def registrar(self, passo):
        self.fechar_texto_corrente()
        passo["espera"] = self.espera_desde_o_passo_anterior()
        self.passos.append(passo)
        print(f"  {len(self.passos):3d}. {passo['tipo']}: "
              + json.dumps({k: v for k, v in passo.items() if k not in ('tipo', 'espera')},
                           ensure_ascii=False))

    def fechar_texto_corrente(self):
        """O texto digitado acumula letra a letra; vira UM passo quando algo o interrompe."""
        if not self.texto_corrente:
            return
        texto = self.texto_corrente
        self.texto_corrente = ""
        passo = {"tipo": "digita", "texto": texto, "espera": self.espera_desde_o_passo_anterior()}
        self.passos.append(passo)
        print(f"  {len(self.passos):3d}. digita: {texto!r}")

    def salvar_recorte_do_clique(self, x, y):
        metade = TAMANHO_DO_RECORTE // 2
        largura_tela, altura_tela = pyautogui.size()
        esquerda = min(max(0, x - metade), largura_tela - TAMANHO_DO_RECORTE)
        topo = min(max(0, y - metade), altura_tela - TAMANHO_DO_RECORTE)
        nome = f"passo-{len(self.passos) + 1:03d}.png"
        pyautogui.screenshot(str(self.pasta / nome),
                             region=(esquerda, topo, TAMANHO_DO_RECORTE, TAMANHO_DO_RECORTE))
        return nome

    # --- mouse -----------------------------------------------------------

    def ao_clicar(self, x, y, botao, apertou):
        if apertou:
            self.inicio_do_arrasto = {
                "x": x, "y": y,
                "botao": NOME_DO_BOTAO.get(botao.name, botao.name),
                "janela": self.titulo_da_janela_ativa(),
                "recorte": self.salvar_recorte_do_clique(x, y),
            }
            return
        inicio = self.inicio_do_arrasto
        self.inicio_do_arrasto = None
        if inicio is None:
            return
        moveu = max(abs(x - inicio["x"]), abs(y - inicio["y"]))
        if moveu > DISTANCIA_MINIMA_DE_ARRASTO:
            self.registrar({"tipo": "arrasto", "de": [inicio["x"], inicio["y"]], "ate": [x, y],
                            "botao": inicio["botao"], "janela": inicio["janela"],
                            "recorte": inicio["recorte"]})
        else:
            self.registrar({"tipo": "clique", "x": inicio["x"], "y": inicio["y"],
                            "botao": inicio["botao"], "janela": inicio["janela"],
                            "recorte": inicio["recorte"]})

    def ao_rolar(self, x, y, dx, dy):
        ultimo = self.passos[-1] if self.passos else None
        recente = time.time() - self.ultimo_tempo < 1.0
        if ultimo and ultimo["tipo"] == "rolagem" and recente and not self.texto_corrente:
            ultimo["cliques"] += dy
            self.ultimo_tempo = time.time()
            return
        self.registrar({"tipo": "rolagem", "x": x, "y": y, "cliques": dy})

    # --- teclado ---------------------------------------------------------

    def ao_apertar_tecla(self, tecla):
        if tecla == TECLA_DE_PARADA:
            return False  # encerra os listeners
        if tecla in MODIFICADORES:
            self.modificadores_apertados.add(MODIFICADORES[tecla])
            return None
        combinando = self.modificadores_apertados - {"shift"}
        if combinando:
            self.registrar({"tipo": "atalho",
                            "teclas": "+".join(sorted(combinando) + [nome_da_tecla(tecla)])})
        elif isinstance(tecla, keyboard.KeyCode):
            if tecla.char:  # tecla morta (acento solto) vem sem char; o acento entra na letra seguinte
                self.texto_corrente += tecla.char
        elif tecla == keyboard.Key.space:
            self.texto_corrente += " "
        else:
            self.registrar({"tipo": "tecla", "tecla": nome_da_tecla(tecla)})
        return None

    def ao_soltar_tecla(self, tecla):
        if tecla in MODIFICADORES:
            self.modificadores_apertados.discard(MODIFICADORES[tecla])

    # --- resultado -------------------------------------------------------

    def salvar(self, nome_da_tarefa):
        self.fechar_texto_corrente()
        largura, altura = pyautogui.size()
        conteudo = {
            "tarefa": nome_da_tarefa,
            "gravado_em": datetime.now().isoformat(timespec="seconds"),
            "tela": [largura, altura],
            "passos": self.passos,
        }
        destino = self.pasta / "passos.json"
        destino.write_text(json.dumps(conteudo, ensure_ascii=False, indent=2), encoding="utf-8")
        return destino


def nome_da_tecla(tecla):
    """Nome no vocabulario do pyautogui, pro reproduz.py usar direto."""
    if isinstance(tecla, keyboard.KeyCode):
        if tecla.char and ord(tecla.char) < 32:  # ctrl+letra chega como caractere de controle
            return chr(ord(tecla.char) + 96)
        return tecla.char or "?"
    return {"cmd": "win"}.get(tecla.name, tecla.name)


def main():
    if len(sys.argv) < 2:
        raise SystemExit("Uso: python gravador.py <nome-da-tarefa>")
    nome = sys.argv[1]
    pasta = Path(__file__).parent / "gravacoes" / nome
    if (pasta / "passos.json").exists():
        raise SystemExit(f"Ja existe gravacao com esse nome em {pasta}. Escolha outro nome ou apague a pasta.")
    pasta.mkdir(parents=True, exist_ok=True)

    print(f"Gravando '{nome}'. Faca a tarefa normalmente e aperte F10 pra encerrar.")
    gravador = Gravador(pasta)
    ouvinte_de_mouse = mouse.Listener(on_click=gravador.ao_clicar, on_scroll=gravador.ao_rolar)
    ouvinte_de_mouse.start()
    with keyboard.Listener(on_press=gravador.ao_apertar_tecla,
                           on_release=gravador.ao_soltar_tecla) as ouvinte_de_teclado:
        ouvinte_de_teclado.join()
    ouvinte_de_mouse.stop()

    destino = gravador.salvar(nome)
    print(f"\n{len(gravador.passos)} passos salvos em {destino}")
    print("Confira o texto digitado no passos.json (acento de tecla morta pode sair errado).")


if __name__ == "__main__":
    main()
