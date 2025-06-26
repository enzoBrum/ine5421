from slr_table import SlrTable
from first_follow import tokenize_production

from argparse import ArgumentParser

# Caminho para o arquivo contendo a gramática desejada
# Assume-se que o símbolo inicial é a cabeça da primeira produção.
GLC_FILE = "input_grammar.txt"

# Arquivo com a tabela SLR.
SLR_FILE = "slr_table.json"

parser = ArgumentParser()
parser.add_argument("--glc-file", default=GLC_FILE)
parser.add_argument("--slr-file", default=SLR_FILE)

args = parser.parse_args()

with open(args.glc_file) as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]

productions = []
for line in lines:
    head, body = line.split("::=")
    rules = [tokenize_production(x.strip()) for x in body.split("|")]
    productions.append((head.strip(), rules))

table = SlrTable.build(productions)
table.pretty_print()

with open(args.slr_file, "w") as f:
    f.write(SlrTable.dumps(table))
