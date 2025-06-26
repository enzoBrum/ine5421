from slr_table import SlrTable
from first_follow import tokenize_production

# Caminho para o arquivo contendo a gramática desejada
# Assume-se que o símbolo inicial é a cabeça da primeira produção.
GLC_FILE = "/home/erb/ufsc/INE5421/t2/input_grammar.txt"

# Arquivo com a tabela SLR.
SLR_FILE = "/home/erb/ufsc/INE5421/t2/slr_table.json"

with open(GLC_FILE) as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]
    
productions = []
for line in lines:
    head, body = line.split("::=")
    rules = [tokenize_production(x.strip()) for x in  body.split("|")]
    productions.append((head.strip(), rules))
    
table = SlrTable.build(productions)
table.pretty_print()

with open(SLR_FILE, "w") as f:
    f.write(SlrTable.dumps(table))
