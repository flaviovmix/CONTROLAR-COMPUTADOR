## Etapa 2: O robô obedece: abre o Chrome na TV

**Objetivo:** ele diz "Python, abre o Chrome" e o Chrome aparece na TV, a tela de trabalho, sem o robô dizer nada.

Tarefas:
- Saber qual é a tela de trabalho. O Windows numera as telas; o robô guarda num arquivo de configuração qual delas é a TV, e na primeira vez mostra o número em cada tela pra ele escolher.
- Abrir o Chrome numa janela nova e pôr a janela na TV, maximizada. Abrir pelo Windows direto (o programa e a posição da janela), não com o mouse.
- Lista fechada de ações: o robô só sabe fazer o que está escrito no código dele. Nenhuma frase ouvida vira comando livre pro Windows.
- Erro (o Chrome não abriu, a TV não está ligada): o robô fala uma frase curta com a voz Maria e escreve o motivo no notebook. Sem erro, fica calado (D5).
- Não tocar na janela da Luna (depende de P2).
- Comando repetido em menos de 3 segundos não abre duas janelas.

**Pronto quando:** ele diz o comando 10 vezes e o Chrome aparece na TV em até 2 segundos nas 10, a janela da Luna não se mexe e não perde a conversa.
