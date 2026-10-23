# CONTROLAR-COMPUTADOR

Gravar uma tarefa repetitiva (cliques, arrastos, teclas, rolagem) uma vez na mão e reexecutar depois. Nasceu da sessão de 29-31/08/2026 (casa no Paint); as pegadinhas de automação de tela estão em `.claude/commands/controlando-teclado-mouse.md`.

## Fluxo

1. **Gravar** — `python gravador.py nome-da-tarefa`, fazer a tarefa normalmente, **F10** encerra. Sai em `gravacoes/nome-da-tarefa/`: `passos.json` + um recorte de tela por clique (o botão apertado).
2. **Conferir** — `python reproduz.py nome-da-tarefa --seco` lista os passos sem mexer em nada.
3. **Reproduzir** — `python reproduz.py nome-da-tarefa`. Esperas entre passos com teto de 3s (`--fiel` respeita as originais). Freio: mouse no canto superior esquerdo aborta.
4. **Virar script de verdade** (o passo que vale) — chamar o Claude apontando a pasta da gravação: ele lê o `passos.json` e escreve um script nomeado, com o que varia (texto, arquivo, data) virando parâmetro e os recortes servindo de `locateOnScreen` pros botões que mudam de lugar. A gravação crua é o rascunho; o script com parâmetro é o produto.

## Arquivos

| Arquivo | Papel |
|---|---|
| `gravador.py` | escuta mouse+teclado (pynput), agrupa digitação em passos de texto, salva recortes |
| `reproduz.py` | reexecuta o `passos.json` (ou `--seco` só lista) |
| `mouse_real.py` | mouse via `SendInput` (clique, arrasto, rolagem) + `ativar_janela` por título |
| `gravacoes/` | uma pasta por tarefa gravada (não versionar as pesadas, decidir caso a caso) |

## Limitações conhecidas

- **Acento de tecla morta** pode sair errado na gravação (o `´` chega sem caractere); conferir o campo `texto` no `passos.json` e corrigir na mão.
- **Coordenada é da tela gravada** (o json guarda a resolução; o reproduz avisa se mudou).
- Menu que abre em posição variável quebra reprodução cega; é o caso de usar o recorte com `locateOnScreen` no script final.
- Gravação captura **tudo** que você digitar até o F10, senha inclusive. Não digitar senha durante a gravação.

Requisitos: Windows, Python 3.12 e os pacotes do `requirements.txt` (a instalação está na seção do robô, abaixo).

## Robô Python (comando por voz)

O robô ouve o mesmo microfone da conversa com a Luna (o ChatGPT por voz) e só age quando a frase inteira é "Python" seguido de um comando da lista dele. O resto da conversa ele ignora. Plano e estado: `plano/html/index.html`.

**Hoje (Etapa 1 do plano):** ele só ouve e mostra, uma linha por frase, a hora, se foi comando ou conversa e o que ouviu. Ainda não abre nada.

| Fale | O que faz |
|---|---|
| "Python, abre o Chrome" | mostra `COMANDO abrir_chrome` (abrir de verdade é a Etapa 2) |

### Instalar (uma vez, na raiz do projeto)

```
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
```

O modelo de voz (português, 31 MB, roda sem internet e sem placa de vídeo), no PowerShell:

```
Invoke-WebRequest https://alphacephei.com/vosk/models/vosk-model-small-pt-0.3.zip -OutFile modelo.zip
Expand-Archive modelo.zip robo\modelos
Remove-Item modelo.zip
```

### Ligar

```
.venv\Scripts\python -m robo --listar-microfones
.venv\Scripts\python -m robo --microfone Realtek
```

Neste computador o microfone padrão do Windows é a placa de captura de vídeo, não um microfone; por isso o `--microfone` com um pedaço do nome. Ctrl+C desliga.

### Provas

```
.venv\Scripts\python -m pytest robo/testes
```

As provas passam cada áudio de `robo/testes/audios/<voz>/comando/` (tem que virar comando) e de `robo/testes/audios/<voz>/conversa/` (não pode virar) pelo mesmo ouvido do microfone. A voz Maria, do Windows, vem no git. A sua voz fica só nesta máquina, gravada com:

```
.venv\Scripts\python -m robo.testes.gravar_minha_voz --microfone Realtek
```
