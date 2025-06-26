from slr_table import SlrTable
from parser import parse
from argparse import ArgumentParser

# Caminho para o arquivo contendo a tabela SLR desejada.
SLR_TABLE = "slr_table.json"

# Caminho para o arquivo contendo a lista de tokens que serão analisados
TOKEN_LIST = "token_list.txt"

# Caminho para o arquivo com a tabela de símbolos
SYMBOL_TABLE = "symbol_table.txt"

cli_parser = ArgumentParser()
cli_parser.add_argument("--slr-table", default=SLR_TABLE)
cli_parser.add_argument("--token-list", default=TOKEN_LIST)
cli_parser.add_argument("--symbol-table", default=SYMBOL_TABLE)

args = cli_parser.parse_args()

with open(args.slr_table) as f:
    table = SlrTable.loads(f.read().strip())

with open(args.token_list) as f:
    token_list = [x.strip() for x in f.readlines() if x.strip()]
with open(args.symbol_table) as f:
    symbol_table = [value.strip().split(":", 1)[1].strip() for value in f.readlines()]

parse(table, token_list, symbol_table)
