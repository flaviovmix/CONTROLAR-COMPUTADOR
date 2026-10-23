"""Liga o robô Python: escuta o microfone e mostra cada frase ouvida.

Etapa 1 do plano: o robô só ouve e mostra, ainda não faz nada.
Uso, na raiz do projeto:
  .venv\\Scripts\\python -m robo --microfone Realtek
  .venv\\Scripts\\python -m robo --listar-microfones
"""
import argparse
import time

from robo.comandos import interpretar_frase
from robo.ouvido import achar_microfone, carregar_modelo, escutar_microfone, listar_microfones


def ler_argumentos():
    leitor = argparse.ArgumentParser(prog="python -m robo", description="O robô Python ouvindo.")
    leitor.add_argument("--microfone", help="um pedaço do nome do microfone (ex.: Realtek)")
    leitor.add_argument("--listar-microfones", action="store_true", help="mostra os microfones e sai")
    return leitor.parse_args()


def mostrar_microfones():
    for indice, nome in listar_microfones():
        print(f"{indice:3}  {nome}")


def mostrar_frase(frase_ouvida, comando):
    hora = time.strftime("%H:%M:%S")
    marca = f"COMANDO {comando.nome}" if comando else "conversa"
    print(f"{hora}  {marca:22}  {frase_ouvida}", flush=True)


def escutar(microfone):
    modelo = carregar_modelo()
    print("Robô Python ouvindo. Ctrl+C desliga.", flush=True)
    try:
        for frase_ouvida in escutar_microfone(modelo, microfone):
            mostrar_frase(frase_ouvida, interpretar_frase(frase_ouvida))
    except KeyboardInterrupt:
        print("Robô desligado.", flush=True)


def main():
    argumentos = ler_argumentos()
    if argumentos.listar_microfones:
        mostrar_microfones()
        return
    escutar(achar_microfone(argumentos.microfone))


if __name__ == "__main__":
    main()
