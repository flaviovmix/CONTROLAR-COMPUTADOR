## Etapa 0: Decisões e a casa do robô ✅ 23/10/2026

**Objetivo:** as decisões dele escritas e um lugar arrumado pro robô antes da primeira linha de código.

Tarefas:
- ✅ (23/10/2026) Escrever as decisões da conversa com a Luna (D1 a D8) e as pendências no `plano.md`.
- ✅ (23/10/2026) Ele respondeu a P1: fica aqui.
- ✅ (23/10/2026) Arrumar a casa: o robô ganhou a pasta `robo/` na raiz do projeto (o gravador e o reprodutor ficam onde estão). `requirements.txt` com versão de cada pacote, que o projeto não tinha (a nota de saúde de 26/09 cobrava). O modelo de voz mora em `robo/modelos/`, fora do git (31 MB pra baixar, 52 MB aberto; o LEIA-ME ensina). `.venv/` fora do git. Seção nova no `LEIA-ME.md`: instalar, ligar, provas e gravar a voz dele.

Padrões do plano (valem até ele confirmar ou trocar):
- Python 3.12, o desta máquina. Ambiente próprio do projeto (`.venv/`, fora do git).
- Reconhecedor: **Vosk** 0.3.45 com o modelo pequeno de português `vosk-model-small-pt-0.3` (Apache 2.0, roda sem internet e sem placa de vídeo). Plano B, se a voz dele não passar na Etapa 1: **faster-whisper**, que ele já usa nos cortes, mais pesado.
- Voz do robô, quando ele precisa falar: a **Maria** do Windows (pt-BR, já instalada).

**Pronto quando:** P1 respondida, a pasta `robo/` existe com `requirements.txt` e o `.gitignore` tira o modelo e o `.venv/`, e o LEIA-ME diz como ligar.
