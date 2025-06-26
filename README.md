Trabalho 2

Alunos: Enzo da Rosa Brum, Sergio Bonini, Kalleo Alexandre Ouriques

O trabalho é composto por quatro arquivos principais:

# Estrutura dos arquivos

### Criados no T1 e modificados agora.
- `src/main.py`, responsável por converter múltiplas expressões regulares em um único AFD. Ele representa a interface de projeto.
- `src/tokenizer.py`, responsável por realizar a análise léxica de uma entrada específica utilizando o AFD gerado. Ele representa a interface de execução.


### Criados no T2
- `t2/interface_projeto`, responsável por gerar uma tabela SLR a partir de uma gramática livre de contexto. Ele representa a interface de projeto.
- `t2/interface_execucao.py`, responsável por realizar a análise sintática.

## Analisador léxico

## Executando a interface de projeto

Para executar `src/main.py`, use o comando `python3 src/main.py`. O arquivo `input-interface-projeto.txt`, cujo caminho está definido na variável `FILE_REGEX` em `src/main.py`, deve conter as expressões regulares a serem convertidas.

Por sua vez, o arquivo `output-interface-projeto.txt`, cujo caminho está definido na variável `FILE_OUTPUT` em `src/main.py`, irá conter o AFD gerado

Tais arquivos também podem ser definidos por linha de comando. Para saber como, use `python3 src/main.py --help`

## Executando a interface de execução

Para executar `src/tokenizer.py`, use o comando `python3 src/tokenizer.py`. O arquivo `output-interface-projeto.txt`, cujo caminho está definido na variável `FILE_AUTOMATO` em `src/tokenizer.py`, deve conter a tabela de análise léxica gerada pela interface de projeto.

O arquivo `input.txt`, cujo caminho está definido na variável `FILE_INPUT` em `src/tokenizer.py`, deve conter a entrada de texto que será análisada.

Por sua vez, o arquivo `symbol_table.txt`, cujo caminho está definido na variável `SYMBOL_TABLE` em `src/tokenizar.py`, irá conter a tabela de símbolos e o
arquivo `token_list.txt`, cujo caminho está definido na variável `TOKEN_LIST` em `src/tokenizer.py` irá conter a lista de tokens.

Tais arquivos também podem ser definidos por linha de comando. Para saber como, use `python3 src/tokenizer.py --help`


## Analisador sintático

## Executando a interface de projeto

Para executar `t2/interface_projeto.py`, use o comando `python3 t2/interface_projeto.py`. O arquivo `input_grammar.txt` cujo caminho está definido na variável `GLC_FILE` em `t2/interface_projeto.py` contém a gramática que define a linguagem.

O arquivo `slr_table.json`, cujo caminho está definido na variável `SLR_TABLE`, conterá a tabela de análise SLR. Ademais, a tabela também é printada no terminal de acordo com o formato nos slides.

Tais arquivos também podem ser definidos por linha de comando. Para saber como, use `python3 t2/interface_projeto.py --help`

## Executando a interface de execução

Para executar `t2/interface_execucao.py`, use o comando `python3 t2/interface_execucao.py`. O arquivo `slr_table.json`, cujo caminho está definido na variável `SLR_TABLE` em `t2/interface_execucao.py`, define a tabela SLR.

O arquivo `token_list.txt`, cujo caminho está especificado em `TOKEN_LIST`, define a lista de tokens análisada (que é saída do analisador léxico).

O arquivo `symbol_table.txt`, cujo caminho está específicado em `SYMBOL_TABLE`, define a tabela de símbolos.

Tais arquivos também podem ser definidos por linha de comando. Para saber como, use `python3 t2/interface_execucao.py --help`
