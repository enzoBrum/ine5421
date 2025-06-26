Trabalho 2

Alunos: Enzo da Rosa Brum, Sergio Bonini, Kalleo Alexandre Ouriques


# Trabalho 1

## Estrutura do projeto

O trabalho é composto por dois arquivos principais: 
- `t2/interface_projeto`, responsável por gerar uma tabela SLR a partir de uma gramática livre de contexto. Ele representa a interface de projeto.
- `t2/interface_execucao.py`, responsável por realizar a análise sintática.

Além disso, também há casos teste de exemplo em `src/test/` para ambos os arquivos.
No caso do `src/test/testMain.py`, há a opção de também desenhar o autômato gerado. Para isso, é necessário instalar o `graphviz` com `pip install graphviz` e `apt install graphviz`.

## Executando a interface de projeto

Para executar `src/main.py`, use o comando `python3 src/main.py`. O arquivo `input-interface-projeto.txt`, cujo caminho está definido na variável `FILE_REGEX` em `src/main.py`, deve conter as expressões regulares a serem convertidas.

Por sua vez, o arquivo `output-interface-projeto.txt`, cujo caminho está definido na variável `FILE_OUTPUT` em `src/main.py`, irá conter o AFD gerado

## Executando a interface de execução

Para executar `src/tokenizer.py`, use o comando `python3 src/tokenizer.py`. O arquivo `output-interface-projeto.txt`, cujo caminho está definido na variável `FILE_AUTOMATO` em `src/tokenizer.py`, deve conter a tabela de análise léxica gerada pela interface de projeto.

O arquivo `input.txt`, cujo caminho está definido na variável `FILE_INPUT` em `src/tokenizer.py`, deve conter a entrada de texto que será análisada.

Por sua vez, o arquivo `output.txt`, cujo caminho está definido na variável `FILE_OUTPUT` em `src/tokenizar.py`, irá conter o resultado da análise léxica.

## Testando o análisador léxico individualmente

Para identificar que padrão cada estado final do autômato representa, utilizamos a seguinte nomenclatura: `<name>__<id-do-estado>`, onde `name` representa o nome do padrão e `id-do-estado` representa o identificador único do estado. 

E.g: `letra__q0,letra__q1,letra__q2`

Cada um dos estados acima é um estado diferente, contudo todos representam o padrão `letra`. Caso o estado final não possua `__`, o analisador léxico irá supor que o nome do estado equivale ao nome do padrão.

E.g: `q0,q1,q2`

Cada um dos estados acima é um estado diferente representando produções diferentes.

# Trabalho 2

## Estrutura do projeto

O trabalho é composto por dois arquivos principais: 
- `src/main.py`, responsável por converter múltiplas expressões regulares em um único AFD. Ele representa a interface de projeto.
- `src/tokenizer.py`, responsável por realizar a análise léxica de uma entrada específica utilizando o AFD gerado. Ele representa a interface de execução.

Além disso, também há casos teste de exemplo em `src/test/` para ambos os arquivos.
No caso do `src/test/testMain.py`, há a opção de também desenhar o autômato gerado. Para isso, é necessário instalar o `graphviz` com `pip install graphviz` e `apt install graphviz`.

## Executando a interface de projeto

Para executar `src/main.py`, use o comando `python3 src/main.py`. O arquivo `input-interface-projeto.txt`, cujo caminho está definido na variável `FILE_REGEX` em `src/main.py`, deve conter as expressões regulares a serem convertidas.

Por sua vez, o arquivo `output-interface-projeto.txt`, cujo caminho está definido na variável `FILE_OUTPUT` em `src/main.py`, irá conter o AFD gerado

## Executando a interface de execução

Para executar `src/tokenizer.py`, use o comando `python3 src/tokenizer.py`. O arquivo `output-interface-projeto.txt`, cujo caminho está definido na variável `FILE_AUTOMATO` em `src/tokenizer.py`, deve conter a tabela de análise léxica gerada pela interface de projeto.

O arquivo `input.txt`, cujo caminho está definido na variável `FILE_INPUT` em `src/tokenizer.py`, deve conter a entrada de texto que será análisada.

Por sua vez, o arquivo `output.txt`, cujo caminho está definido na variável `FILE_OUTPUT` em `src/tokenizar.py`, irá conter o resultado da análise léxica.

## Testando o análisador léxico individualmente

Para identificar que padrão cada estado final do autômato representa, utilizamos a seguinte nomenclatura: `<name>__<id-do-estado>`, onde `name` representa o nome do padrão e `id-do-estado` representa o identificador único do estado. 

E.g: `letra__q0,letra__q1,letra__q2`

Cada um dos estados acima é um estado diferente, contudo todos representam o padrão `letra`. Caso o estado final não possua `__`, o analisador léxico irá supor que o nome do estado equivale ao nome do padrão.

E.g: `q0,q1,q2`

Cada um dos estados acima é um estado diferente representando produções diferentes.