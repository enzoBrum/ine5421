from determinizer import determinize
from draw import desenhar_automato
from finite_automaton import FiniteAutomaton
from generateAFN import ThompsonAFN
from transformER import RegEx

# regExpressões fornecidas
regExpressoes = {
    "id": "[a-zA-Z]([a-zA-Z]|[0-9])*",
    "num": "[1-9]([0-9])*|0",
    "er1": "a?(a|b)+",
    "er2": "(a|b)*",
}

# Resultado
for nome, rawRegex in regExpressoes.items():
    print(f"nome -> {nome}\nrawRegex -> {rawRegex}")

    regex = RegEx(rawRegex)

    print("Postfix ->", regex.transformedRegEx)
    afn = ThompsonAFN(regex.transformedRegEx)
    # desenhar_automato(nome, afn.transitions)
    # print("First state ->", afn.start)
    # print("Final state ->", afn.final)
    # print("Transitions ->", afn.transitions)
    determinzed_afn = determinize(FiniteAutomaton.from_thompson_afn(afn))

    print(FiniteAutomaton.dumps(determinzed_afn))

    # desenhar_automato(f"{nome}-determinizado", determinzed_afn.transictions)
