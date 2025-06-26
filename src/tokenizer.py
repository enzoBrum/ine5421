from argparse import ArgumentParser

from finite_automaton import FiniteAutomaton


# Arquivo contendo a saída de main.py com a tabela de análise léxica.
FILE_AUTOMATO = "output-interface-projeto.txt"

# Arquivo contendo os inputs a serem analisados
FILE_INPUT = "input.txt"

# Arquivo onde o resultado da analise será escrito.
FILE_SYMBOL_TABLE = "symbol_table.txt"
FILE_TOKEN_LIST = "token_list.txt"

parser = ArgumentParser()
parser.add_argument("--file-automato", default=FILE_AUTOMATO)
parser.add_argument("--file-input", default=FILE_INPUT)
parser.add_argument("--file-symbol-table", default=FILE_SYMBOL_TABLE)
parser.add_argument("--file-token-list", default=FILE_TOKEN_LIST)


def classify(finite_automaton: FiniteAutomaton, word: str) -> str:
    state = finite_automaton.initial_state
    for ch in word:

        # Aqui estamos fazendo indexação por [0] só por conveniência de ter uma classe só pra AFND e AFD.
        # Na realidade, como ele esta determinizado, a lista sempre será de tamanho 1.
        state = finite_automaton.transitions[state].get(ch, [None])[0]
        if state is None:
            break

    try:
        return next(iter(finite_automaton.final_states_to_pattern[state]))
    except:
        print(f"Palavra inválida: {word}")
        exit(0)


def get_symbol_table(finite_automaton: FiniteAutomaton, words: list[str]) -> str:
    line_counter = 1
    added_token = {}

    tokens = []
    symbol_table = []
    for word in words:
        att_value = word.strip()
        classification = classify(finite_automaton, att_value)

        if att_value not in added_token.keys():
            new_att = {}
            new_att["line"] = line_counter

            new_att["classification"] = classification

            symbol_table.append(str(line_counter) + ": " + att_value)

            added_token[att_value] = new_att
            line_counter += 1

        tokens.append(f"<{classification}, {added_token[att_value]['line']}>")

    return symbol_table, tokens


if __name__ == "__main__":
    args = parser.parse_args()
    with open(args.file_automato, "r") as f:
        determinized_automato = FiniteAutomaton.loads(f.read())

    with open(args.file_input, "r") as f:
        words = [word for line in f for word in line.strip().split() if word]

    symbol_table, tokens = get_symbol_table(determinized_automato, words)

    symbol_table = "\n".join(symbol_table)
    tokens = "\n".join(tokens)

    print_result = (
        "====== Tabela de Símbolos ======\n"
        + symbol_table
        + "\n\n"
        + "====== Lista de Tokens ======\n"
        + tokens
    )
    print(print_result)

    with open(args.file_symbol_table, "w") as f:
        f.write(symbol_table)

    with open(args.file_token_list, "w") as f:
        f.write(tokens)
