from argparse import ArgumentParser

from finite_automaton import FiniteAutomaton

# Arquivo contendo a saída de main.py com a tabela de análise léxica.
FILE_AUTOMATO = "output-interface-projeto.txt"

# Arquivo contendo os inputs a serem analisados
FILE_INPUT = "input.txt"

# Arquivo onde o resultado da analise será escrito.
FILE_OUTPUT = "output.txt"

def classify(finite_automaton: FiniteAutomaton, word: str) -> str:
    state = finite_automaton.initial_state
    for ch in word:

        # Aqui estamos fazendo indexação por [0] só por conveniência de ter uma classe só pra AFND e AFD.
        # Na realidade, como ele esta determinizado, a lista sempre será de tamanho 1.
        state = finite_automaton.transitions[state].get(ch, [None])[0]
        if state is None:
            break
    return (
        "Não reconhecido"
        if state not in finite_automaton.final_states
        else next(iter(finite_automaton.final_states_to_pattern[state]))
    )


def get_symbol_table(finite_automaton: FiniteAutomaton, words: list[str]) -> str:
    return [f"<{w.strip()}, {classify(finite_automaton, w.strip())}>" for w in words]


if __name__ == "__main__":
    with open(FILE_AUTOMATO, "r") as f:
        determinized_automato = FiniteAutomaton.loads(f.read())

    with open(FILE_INPUT, "r") as f:
        words = [line.strip() for line in f.readlines() if line]

    out = "\n".join(get_symbol_table(determinized_automato, words))
    print(out)
    
    with open(FILE_OUTPUT, "w") as f:
        f.write(out)
