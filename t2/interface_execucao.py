from slr_table import SlrTable
from parser import parse

# Caminho para o arquivo contendo a tabela SLR desejada.
SLR_TABLE = "./slr_table.json"

# Caminho para o arquivo contendo a lista de tokens que serão analisados
TOKEN_LIST = "./token_list.txt"

with open(SLR_TABLE) as f:
    table = SlrTable.loads(f.read().strip())

with open(TOKEN_LIST) as f:
    token_list = [x.strip() for x in f.readlines() if x.strip()]

parse(table, token_list)