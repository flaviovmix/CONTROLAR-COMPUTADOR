## Etapa 1: O robô ouve

**Objetivo:** o robô escuta o microfone o tempo todo, junto com a Luna, e sabe separar "Python, abre o Chrome" da conversa normal. Nesta etapa ele ainda não faz nada: só mostra na tela do notebook o que ouviu.

O que já se sabe (prova de 23/10/2026, com as frases ditas pela voz Maria do Windows, gravadas e passadas ao Vosk):
- No vocabulário do modelo pequeno **existem** "python", "abre", "explorer", "email", "print", "luna", "manda", "pasta". **Não existem** "chrome" nem "e-mail" com hífen.
- Ouvindo livre, o modelo erra quase tudo ("Python, abre o Chrome" virou "fale abril"). Com a **lista fechada de frases** (o modo de gramática do Vosk) acertou os quatro comandos, com uma falha que importa: não ouviu o "Python" do começo em nenhum deles. A Maria fala "Python" do jeito dela, e o Flávio fala "páiton"; só a voz dele decide.
- A frase de conversa "Luna, o que você acha do Python?" não virou comando.
- Como "Chrome" não está no vocabulário, a frase da lista é "abre o cromo" (o som é o mesmo). Se não bastar, "abre o navegador".

Segunda prova (23/10/2026, à tarde): a Maria falando **"Páiton, abre o crôme"**, escrito do jeito que brasileiro fala, foi ouvida como "python abre o cromo" nas 3 grafias testadas. Com "Python" escrito em inglês ela fala algo que o modelo ouve como "pai". A conversa "Eu gosto de programar em Páiton, abre o crôme depois" veio como "[unk] python abre o cromo": a regra de começar pelo nome segurou. Esses áudios viraram as provas da voz Maria.

Achado da máquina (23/10/2026): **o microfone padrão do Windows neste computador é a placa de captura de vídeo** ("Interface de áudio digital", Display capture-UVC05), não um microfone. O robô e o gravador da voz escolhem o microfone por um pedaço do nome (`--microfone Realtek`). O Realtek abriu a 16 kHz e captou som (nível médio 190, pico 3.084 em 4 segundos de sala).

Tarefas:
- ✅ (23/10/2026) Ouvir o microfone em modo compartilhado, escolhido pelo nome. Falta conferir com a Luna aberta ao mesmo tempo, que é o caso dele.
- ✅ (23/10/2026) Ouvir com a lista fechada de frases, mais o "[unk]" que pega todo o resto da conversa.
- ✅ (23/10/2026) Comando só vale se a frase inteira for o nome mais um comando da lista. Frase sem o nome, com o nome no meio ("o que você acha do Python") ou com conversa colada depois é conversa.
- ✅ (23/10/2026) Mostrar numa linha por frase: a hora, se foi comando ou conversa e o que ouviu (`python -m robo`).
- ✅ (23/10/2026) Arnês de prova que roda por um comando, sem microfone (`python -m pytest robo/testes`): a regra pura e os áudios de cada voz em `audios/<voz>/comando` e `audios/<voz>/conversa`. A voz dele entra sozinha quando existir.
- Gravar a voz dele (`python -m robo.testes.gravar_minha_voz --microfone Realtek`): 10 vezes "Python, abre o Chrome" e 10 frases de conversa, entre elas "Meu pai abre o Chrome todo dia", "Luna, abre o Chrome" e "Python é o nome do robô". Se o "Python" dele não for ouvido, testar o plano B (faster-whisper ouvindo só o que vem depois de uma pausa) e anotar aqui qual ficou e por quê.

**Pronto quando:** na voz dele, 10 de 10 "Python, abre o Chrome" aparecem como comando, nenhuma das 10 frases de conversa vira comando, e isso vale com a conversa da Luna aberta ao mesmo tempo.
