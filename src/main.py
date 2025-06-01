from determinizer import determinize
from draw import desenhar_automato
from finite_automaton import FiniteAutomaton
from generateAFN import ThompsonAFN
from transformER import RegEx

# regExpressões fornecidas
regExpressoes = {
    # "id": "[a-zA-Z]([a-zA-Z]|[0-9])*",
    # "num": "[1-9]([0-9])*|0",
    "er1": "a?(a|b)+",
    "er2": "(a|b)*",
}

automatos: dict[str, FiniteAutomaton] = {}

# Resultado
for nome, rawRegex in regExpressoes.items():
    print(f"nome -> {nome}\nrawRegex -> {rawRegex}")

    regex = RegEx(rawRegex)

    print("Postfix ->", regex.transformedRegEx)
    afn = FiniteAutomaton.from_thompson_afn(ThompsonAFN(regex.transformedRegEx))
    automatos[nome] = afn
    desenhar_automato(
        nome,
        afn.transictions,
        afn.initial_state,
        afn.final_states,
    )

automato = FiniteAutomaton.join_automatons(automatos)

desenhar_automato(
    "nao-determinizado",
    automato.transictions,
    automato.initial_state,
    automato.final_states,
)

determinized_automato = determinize(automato)
print(FiniteAutomaton.dumps(determinized_automato))

desenhar_automato(
    "determinizado",
    determinized_automato.transictions,
    determinized_automato.initial_state,
    determinized_automato.final_states,
)

print(
    "\n".join(
        f"{k} -> {','.join(v)}"
        for k, v in determinized_automato.final_states_to_pattern.items()
    )
)
