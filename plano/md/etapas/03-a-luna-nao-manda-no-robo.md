## Etapa 3: A Luna não manda no robô

**Objetivo:** o robô obedece só ao Flávio, nunca à Luna. Na conversa de 23/10 a própria Luna disse em voz alta *"Minha sugestão continua sendo 'Python, abre o Chrome.'"*: com caixa de som, o microfone pega a fala dela e o robô obedeceria.

Tarefas:
- Os dois modos, com escolha (P3, resolvida em 23/10/2026): fone e caixa de som. O robô guarda o modo escolhido e troca sem reiniciar.
- Com fone de ouvido o problema some: a voz dela não chega ao microfone. Provar mesmo assim.
- Com caixa de som: o robô não obedece enquanto a janela da Luna está tocando som. O Windows mede o volume de cada programa; ler o do navegador da Luna e travar o robô enquanto ela fala. Conferir na documentação do Windows antes de prometer.
- Uma frase pras instruções da Luna: quando ele começar com "Python", ela fica quieta, porque não é com ela. Ela também ouve o comando e hoje responderia.

**Pronto quando:** a Luna diz o comando 5 vezes (pela caixa, se for caixa) e o robô não obedece nenhuma; logo depois ele diz e o robô obedece.
