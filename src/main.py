from determinizer import determinize
from finite_automaton import FiniteAutomaton
from generateAFN import ThompsonAFN
from transformER import RegEx

# Arquivo com as expressões regulares
FILE_REGEX = f"input-interface-projeto.txt"

# Arquivo onde a tabela de análise léxica será escrita.
FILE_OUTPUT = "output-interface-projeto.txt"

with open(FILE_REGEX, "r") as f:
    lines = [line.strip().split(":", 1) for line in f.readlines() if line.strip()]
    regexes = {line[0].strip(): line[1].strip() for line in lines if len(line) > 1}

automatos = {}
for nome, rawRegex in regexes.items():
    nome = nome.strip()
    regex = RegEx(rawRegex.strip())
    afn = FiniteAutomaton.from_thompson_afn(ThompsonAFN(regex.transformedRegEx))
    automatos[nome] = afn

automato = FiniteAutomaton.join_automatons(automatos)
determinized_automato = determinize(automato)
out=FiniteAutomaton.dumps(determinized_automato)

print(out)

with open(FILE_OUTPUT, "w") as f:
    f.write(out)