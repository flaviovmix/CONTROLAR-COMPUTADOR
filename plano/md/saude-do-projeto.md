# Nota de saúde do projeto (0 a 10)

Ferramenta de diagnóstico. Não é etapa, não tem "pronto quando", e roda quando alguém quiser saber como o projeto está: antes de retomar depois de meses, antes de abrir pro primeiro usuário, ou quando bateu a sensação de que a casa desarrumou.

**Funciona em qualquer projeto**, tenha ele nascido deste molde ou não. Projeto que nunca viu o molde só vai tirar nota baixa em algumas dimensões, e é exatamente essa a informação.

---

## As três regras de quem aplica

1. **Não corrigir durante a análise.** Vale a mesma regra da Etapa 13: cada achado ganha destino decidido junto com o dono (corrigir já, pegar carona numa etapa, ou entrar na fila de erros). Quem corrige calado no meio da varredura perde a medida e não termina nenhuma das duas coisas.
2. **Nota sem evidência não vale.** Toda nota abaixo de 8 aponta arquivo e linha, ou o comando que provou. "Parece frágil" não é achado.
3. **Medir o que está lá, não o que se lembra.** Ler o código, rodar o que der pra rodar. Impressão de sessão antiga é a principal fonte de nota errada.

---

## As 8 dimensões

Cada uma vale de 0 a 10. O que cada nota significa está na régua do fim.

### 1. Segurança
Segredo versionado (senha, token, chave em arquivo do repo ou em migration). Autorização conferida rota a rota, com o padrão sendo negar. Senha com hash forte. Freio de força bruta no login. Upload validado por assinatura do arquivo, não pelo tipo declarado. Dependência com vulnerabilidade aberta.
**Prova rápida:** buscar por senha e chave no histórico do git; bater três papéis (anônimo, comum, admin) contra uma rota administrativa; conferir o alerta de dependência do repo.

### 2. Teste
Existe arnês rodando por um comando. Ele cobre o caminho crítico: autenticação, salvar com validação recusando, excluir. Roda contra banco de verdade. Bug já corrigido deixou teste que o reproduz.
**Prova rápida:** rodar a suíte. Se não roda por um comando, a nota já começa baixa, porque teste que ninguém consegue rodar não protege ninguém.

### 3. Legibilidade
Função com uma responsabilidade e tamanho que cabe na tela. Nome que dispensa comentário. HTML semântico. CSS e JS em arquivo por componente, não dentro do template. Pasta que um humano entende sem buscar.
**Prova rápida:** contar as funções maiores que ~60 linhas e as linhas de estilo e script inline dentro de template.

### 4. Duplicação
Clone do mesmo padrão (controller, modal, store, formulário, mapeador). Decisão repetida em N lugares: mudar o texto de um aviso comum exige lembrar de quantos arquivos?
**Prova rápida:** escolher um aviso ou uma regra que aparece em vários lugares e contar em quantos arquivos ela mora.

### 5. Banco e dados
Migrations versionadas e nunca editadas depois de aplicadas. Banco novo sobe do zero sem passo manual. Índice nas chaves estrangeiras e nas colunas de busca. Regra de exclusão pensada. Enum do código batendo com a restrição do banco.
**Prova rápida:** recriar o banco do zero. Se precisar de passo manual, a dimensão não passa de 5.

### 6. Deploy e operação
Procedimento de subir escrito e testado. Caminho de volta (rollback) que alguém já usou. Backup rodando, guardado fora da máquina, restaurado ao menos uma vez, com alerta quando falha. Monitoramento que avisa antes do usuário avisar.
**Prova rápida:** perguntar quando foi a última restauração de backup testada. "Nunca" é nota 3 ou menos, porque backup nunca testado não é backup.

### 7. Interface
Sem estouro horizontal nos 4 tamanhos. Acessibilidade: rótulo ligado ao campo, foco visível, alcançável por teclado. Estado vazio tratado. Imagem com dimensão declarada. Política de conteúdo (CSP) ligada.
**Prova rápida:** medir uma página pública e uma de painel num medidor de acessibilidade, e abrir as duas no tamanho de celular.

### 8. Registro
O plano (ou o README) reflete o que existe hoje. Decisões escritas com o porquê. Fila de erros viva. README ensina alguém de fora a subir o projeto do zero.
**Prova rápida:** seguir o README numa máquina limpa, ou ao menos ler se ele menciona os passos que a versão atual precisa.

---

## Como fecha a nota final

Média simples das oito, **com um freio**: se qualquer dimensão ficar em 3 ou menos, a nota final não passa de 5, por mais alto que esteja o resto. Projeto com segredo exposto em produção não é um "8 com uma ressalva", e média sozinha esconde exatamente esse tipo de buraco.

| Nota | O que significa |
|---|---|
| 9-10 | saudável. Dá pra crescer sem medo |
| 7-8 | bom, com dívida conhecida e escrita |
| 5-6 | funciona, mas cada mudança custa mais que devia |
| 3-4 | a casa desarrumou. Precisa de etapa dedicada antes de feature nova |
| 0-2 | risco real de perder dado, vazar dado ou não conseguir mudar |

---

## O que entregar

Uma tabela e três linhas de texto. Nada mais:

```markdown
| # | Dimensão | Nota | O que puxou pra baixo (arquivo:linha) |
|---|---|---|---|
| 1 | Segurança | 4 | senha no repo em V3__seed.sql:12 |
...

**Nota final: X/10** (freio aplicado: sim/não, por qual dimensão)

**As três coisas que mais sobem a nota:** ...
**O que NÃO vale mexer agora:** ...
```

A linha do que não vale mexer agora é tão importante quanto as outras. Varredura sem prioridade vira lista de 40 itens que ninguém ataca, e a casa segue desarrumada com um relatório em cima.

---

## Resultado

**Auditado em:** 26/09/2026

| # | Dimensão | Nota | O que puxou pra baixo (arquivo:linha) |
|---|---|---|---|
| 1 | Segurança | 5 | o freio de emergência não cobre passo de mouse: `reproduz.py:21` liga o `pyautogui.FAILSAFE`, mas clique, arrasto e rolagem saem por `SendInput` direto (`reproduz.py:63`, `:66` e `:68` chamando `mouse_real.py:56`), e o pyautogui só confere o canto dentro das funções dele (`site-packages/pyautogui/__init__.py:593`; o `size()` da `:777` não confere). Uma gravação só de mouse, sem troca de janela, roda inteira sem freio, e o `LEIA-ME.md:9` promete o contrário. Além disso, o texto digitado vai em texto puro pro `passos.json` (`gravador.py:132`, `:155`) e pro console (`gravador.py:72`), cada clique salva um recorte da tela (`gravador.py:80`), e a proteção é só o aviso do `LEIA-ME.md:26`; o nome da tarefa vira caminho sem validação (`gravador.py:172`, `reproduz.py:27`), então `..` ou caminho absoluto grava e reproduz fora de `gravacoes/`; e não há arquivo de dependências com versão, então não há alerta a conferir. A favor: nenhum segredo no git (`git log --all -p` atrás de senha, password, token, secret e chave só acha o aviso do LEIA-ME), `gravacoes/` fora do repositório (`.gitignore:2`, e `git ls-files` confirma), e a única gravação no disco é o `exemplo`, sem nada sensível |
| 2 | Teste | 1 | não existe teste nenhum: `git ls-files` lista só os três `.py`, o LEIA-ME e o `.gitignore`. O `--seco` (`reproduz.py:91`) é conferência manual, não teste, e o `gravacoes/exemplo/passos.json`, que serviria de caso, fica fora do git (`.gitignore:2`). Há lógica pura que dava pra testar sem tocar no mouse e que ninguém cobre: o nome da tecla (`gravador.py:159`), o agrupamento da digitação (`:64`), clique contra arrasto (`:99`), a normalização 0..65535 (`mouse_real.py:59`) e o despacho por tipo (`reproduz.py:59`). O furo do freio da linha acima é exatamente o que um teste do `executar` com mouse de mentira pegaria |
| 3 | Legibilidade | 9 | medido por `ast`, sem executar: 28 funções, nenhuma acima de 30 linhas; a maior é o `main` de `reproduz.py:80` (29 linhas, junta argumento, modo seco, aviso de tela e o laço). Esperas soltas sem nome (`mouse_real.py:77`, `:79`, `:100`, `:110`, `:129`, `reproduz.py:55`) e um `except Exception` que engole o motivo (`mouse_real.py:127`). Nomes em português que dizem o que fazem e docstring com o porquê onde a decisão não é óbvia (`mouse_real.py:3`, `reproduz.py:48`) |
| 4 | Duplicação | 8 | o formato do `passos.json` não mora num lugar só: os tipos de passo são escritos em `gravador.py:70` a `:136` e lidos em `reproduz.py:61` a `:74`, e os nomes dos botões vivem em `gravador.py:32` e `mouse_real.py:29`; renomear um tipo pede lembrar de dois ou três arquivos. O caminho `gravacoes/<nome>` se repete em `gravador.py:172` e `reproduz.py:27` |
| 5 | Banco e dados | - | não se aplica: não há banco; o dado é um `passos.json` por gravação, local e fora do git |
| 6 | Deploy e operação | - | não se aplica: ferramenta local rodada na própria máquina, nada sobe pra servidor; as gravações são rascunho local por decisão (`.gitignore:1`) |
| 7 | Interface | - | não se aplica: linha de comando, sem tela web nem janela própria |
| 8 | Registro | 6 | os requisitos (`LEIA-ME.md:28`) não citam o Pillow: no Python 3.12 desta máquina o pyscreeze 1.0.1 não o puxa (o `METADATA` dele só pede Pillow até o 3.11, e nenhuma outra dependência pede), então numa máquina limpa o recorte de `gravador.py:80` falha no primeiro clique e, como o ouvinte de mouse é parado sem `join` (`gravador.py:184`), a gravação segue só com o teclado; também não dizem que é só Windows (`mouse_real.py:56`) nem a versão do Python. O `LEIA-ME.md:19` manda decidir caso a caso o que versionar em `gravacoes/`, mas o `.gitignore:2` tira a pasta inteira, inclusive o `exemplo`. As pegadinhas citadas em `LEIA-ME.md:3` e `mouse_real.py:8` moram em `c:\src\.claude\commands\`, fora do repositório, e quem clona do GitHub não as acha. A favor: o LEIA-ME bate com o código no fluxo e nas opções, e as limitações conhecidas estão escritas (`LEIA-ME.md:21` a `:26`) |

**Nota final: 5,0/10** (freio aplicado: sim, pela Teste com 1; a média simples das 5 dimensões que se aplicam, sem Banco, Deploy e Interface, daria 5,8)

**As três coisas que mais sobem a nota:** um arnês que roda por um comando (`python -m pytest`) e cobre a lógica pura sem mexer no mouse (nome da tecla, agrupamento de texto, clique contra arrasto, normalização do `mover_para` com tela de mentira e o `executar` com `mouse_real` e `pyautogui` trocados por dublê), que tira a Teste do 1 e solta o freio da nota; fazer o freio valer pra passo de mouse (conferir o canto antes de cada passo no laço de `reproduz.py:103` e dentro do `deslizar_ate`, com o teste que prova) e recusar nome de tarefa com `..` ou caminho absoluto, que levam a Segurança a 7 ou mais; e uma passada no LEIA-ME: Pillow, Windows e a versão do Python nos requisitos (ou um `requirements.txt` com versão), a frase do `gravacoes/` batendo com o `.gitignore` (ou versionar só o `exemplo`), e as pegadinhas trazidas pra dentro do repositório ou citadas pelo caminho completo.

**O que NÃO vale mexer agora:** legibilidade e duplicação estão em 9 e 8 e não pedem nada. Não vale criar um módulo de contrato do `passos.json` pra dois leitores: ele passa a valer quando nascer o terceiro, o gerador de "script de verdade" do `LEIA-ME.md:10`. Também não vale cifrar as gravações (ferramenta de uso próprio, fora do git e com aviso escrito) nem dar suporte a vários monitores agora: o `mover_para` normaliza pela tela principal (`mouse_real.py:61`), mas esta máquina tem um monitor só (`GetSystemMetrics(80)` devolve 1).
