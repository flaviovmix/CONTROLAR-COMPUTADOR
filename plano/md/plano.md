# Plano: CONTROLAR-COMPUTADOR · o robô Python por voz

**Tipo:** app de uso próprio

**Saída:** ../html

O projeto já tinha o gravador e o reprodutor de mouse e teclado (31/08/2026). Este plano é da parte nova: o **robô "Python"**, que ouve o mesmo microfone da conversa do Flávio com a Luna (o ChatGPT por voz) e obedece quando ouve o próprio nome. Nasceu em 23/10/2026, do prompt "COMPUTADOR POR VOZ" (cartão 105 do quadro CLAUDE CODE) e da conversa dele com a Luna (o link fica na memória do Claude, que é privada: este repositório é público).

Índice do plano. **É o único arquivo lido em toda sessão**; o detalhe mora em `etapas/`, e só a etapa atual é carregada.

---

## Decisões

Decisões **travadas**, tiradas da conversa de 23/10/2026 com a palavra dele. Se a realidade derrubar uma, a nova entra com data e o motivo da virada.

- D1. (23/10/2026) Ele conversa com a Luna e o robô ouve o mesmo microfone, em paralelo. A Luna não fica no meio e não precisa saber o que o robô fez: *"o meu microfone vai tá tanto com você, quanto nesse aplicativozinho que vai fazer as coisas que eu preciso"*.
- D2. (23/10/2026) O robô se chama **Python** e só age quando ouve "Python" mais o comando. Sem o nome, não faz nada.
- D3. (23/10/2026) De graça e no Windows: reconhecedor de fala no próprio computador, sem outra IA e sem pagar por minuto (*"vamo deixá a versão [...] pro Windows gratuita"*).
- D4. (23/10/2026) Uma ordem por vez, pra validar a ideia. A primeira é **"Python, abre o Chrome"**; depois "vai no meu email" e "abre o Explorer e cria uma pasta".
- D5. (23/10/2026) O robô trabalha calado, porque ele vê a tela. Só fala em erro ou antes de ação perigosa.
- D6. (23/10/2026) "Python, manda um print pra Luna" tira foto **só da tela de trabalho** e tenta pôr na conversa sozinho.
- D7. (23/10/2026) Apagar, enviar ou fechar sem salvar: o robô confirma por voz antes.
- D8. (23/10/2026) Montagem: notebook com a tela dele (bastidores), uma tela com a Luna e uma TV no meio, onde o robô mexe. Computador só pro robô é o plano B.

## Pendências

Cada uma diz **em que etapa trava**.

- ~~P1. O robô mora aqui, no CONTROLAR-COMPUTADOR, que já tem o mouse de verdade e o git com GitHub, ou num projeto separado? Coloquei aqui pra não repetir o código do mouse. **Trava a Etapa 0.**~~ Resolvida em 23/10/2026: fica aqui (resposta "A").
- P2. Onde a Luna roda: no navegador ou no app do ChatGPT do Windows? A página de ajuda da OpenAI (lida em 23/10/2026) ensina a conversa por voz só na web e no celular; a voz do app de computador é outra coisa (comandar agentes, preço à parte). Proposta: a Luna no **Edge**, e o robô só mexe no Chrome, assim nunca toca na conversa dela por engano. **Trava a Etapa 2.**
- ~~P3. Fone de ouvido ou caixa de som? Com caixa, o robô ouve a Luna, e ela mesma disse "Python, abre o Chrome" em voz alta na conversa de 23/10. **Trava a Etapa 3.**~~ Resolvida em 23/10/2026: os dois, com escolha (resposta "escolher", entendida como o botão de saída do som do telão do condomínio). A Etapa 3 faz a trava do modo caixa e a troca entre os modos.
- P4. "Vai no meu email": qual e-mail e qual conta abre. **Trava a Etapa 4.**
- P5. "Cria uma pasta": onde a pasta nasce e como ele diz o nome dela. **Trava a Etapa 4.**
- P6. Quais comandos contam como perigosos (a lista que pede confirmação). **Trava a Etapa 6.**
- P7. Qual notebook: tem placa de vídeo? Tem saída pra duas telas além da dele? **Trava a Etapa 7.**
- ~~P8. A segunda conversa com a Luna (23/10) foi com o primeiro prompt colado, sem o plano. Nela a Luna propôs, e ele respondeu "Tá bom": comando sem o nome ("você fala 'abre o Chrome'"), o robô perguntando *"vou abrir o Chrome, ok?"* antes de cada um e respondendo *"não entendi"* ao que não for comando. Bate de frente com D2 e D5. Proposta: ficam D2 e D5, porque o robô ouve a conversa inteira com a Luna e, sem o nome, qualquer "abre o Chrome" dito na conversa vira ordem, e o "não entendi" falaria por cima de cada frase. **Trava a Etapa 1.**~~ Resolvida em 23/10/2026: ele escolheu ficar com D2 e D5 (só age com "Python" e trabalha calado).

---

## Status das etapas

Ao fechar uma etapa, marcar `✅ + data` **aqui e no arquivo dela**.

| # | Etapa | Status | Última mexida |
|---|---|---|---|
| 0 | Decisões e a casa do robô | ✅ 23/10/2026 | 23/10/2026 |
| 1 | O robô ouve | em andamento, 5 de 6 | 23/10/2026 |
| 2 | O robô obedece: abre o Chrome na TV | não iniciada | |
| 3 | A Luna não manda no robô | não iniciada | |
| 4 | Mais comandos, um de cada vez | não iniciada | |
| 5 | O print pra Luna | não iniciada | |
| 6 | Confirmação por voz antes do perigo | não iniciada | |
| 7 | O estúdio montado e o ensaio | não iniciada | |

A Etapa 1 está construída e provada com a voz Maria do Windows; falta a prova com a voz dele, gravada por ele.

O gravador e o reprodutor de 31/08 ficam como estão; a nota de saúde de 26/09 (5,0) é deles e aponta dois furos que este plano conserta quando passar por eles: o freio de emergência que não vale pro mouse de verdade e o mouse que só conhece a tela principal (Etapa 5).
