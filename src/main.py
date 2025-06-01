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

automatos: list[FiniteAutomaton] = []

# Resultado
for nome, rawRegex in regExpressoes.items():
    print(f"nome -> {nome}\nrawRegex -> {rawRegex}")

    regex = RegEx(rawRegex)

    print("Postfix ->", regex.transformedRegEx)
    afn = ThompsonAFN(regex.transformedRegEx)
    automatos.append(FiniteAutomaton.from_thompson_afn(afn))
    # desenhar_automato(
    #    nome,
    #    automatos[-1].transictions,
    #    automatos[-1].initial_state,
    #    automatos[-1].final_states,
    # )

automato = FiniteAutomaton.join_automatons(automatos)

# desenhar_automato(
#    "nao-determinizado",
#    automato.transictions,
#    automato.initial_state,
#    automato.final_states,
# )

determinized_automato = determinize(automato)
print(FiniteAutomaton.dumps(determinized_automato))

# desenhar_automato(
#    "determinizado",
#    determinized_automato.transictions,
#    determinized_automato.initial_state,
#    determinized_automato.final_states,
# )
