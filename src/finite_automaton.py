"""
Contém a classe utilizada para representar autômatos finitos.
"""

# Mapeia um estado à um dicionário cuja chave é uma letra do alfabeto e valor é a lista de
# estados alcançados quando se utiliza essa letra.
#
# e.g: transictions["0"] = {"a": ["0", "1"]} -> A partir do estado "0", é possível alcançar os estados "0" e "1" utilizando a letra "a"
Transictions = dict[str, dict[str, list[str]]]

# Símbolo usado para representar o vazio.
EPSILON = "ε"


class FiniteAutomaton:
    """
    Classe representando um autômato finito.
    """

    states: set[str]
    alphabet: set[str]

    transictions: Transictions

    initial_state: str
    final_states: set[str]

    def __init__(
        self,
        states: set[str],
        alphabet: set[str],
        transictions: Transictions,
        initial_state: str,
        final_states: str,
    ):
        self.states = states
        self.alphabet = alphabet
        self.transictions = transictions
        self.initial_state = initial_state
        self.final_states = final_states

    @staticmethod
    def dumps(finite_automaton: "FiniteAutomaton") -> str:
        ret = (
            f"{len(finite_automaton.states)}\n"
            f"{finite_automaton.initial_state}\n"
            f"{','.join(sorted(finite_automaton.final_states))}\n"
            f"{','.join(sorted(finite_automaton.alphabet))}\n"
        )

        for origin_state, letter_dict in finite_automaton.transictions.items():
            for letter, target_states in letter_dict.items():
                for target in target_states:
                    ret += f"{origin_state},{letter},{target}\n"
        return ret

    @staticmethod
    def loads(finite_automaton_str: str) -> "FiniteAutomaton":
        lines = [x for x in finite_automaton_str.splitlines() if len(x.strip()) > 0]

        assert (
            len(lines) >= 4
        ), "Um autômato finito precisa conter ao menos o número de estados, o estado inicial, o alfabeto e os estados finais"

        initial_state = lines[1].strip()
        final_states = {x.strip() for x in lines[2].split(",")}
        alphabet = {x.strip() for x in lines[3].split(",")}
        transictions: Transictions = {}
        states = set()

        for line in lines[4:]:
            origin, letter, target = [x.strip() for x in line.split(",")]
            states.add(origin)
            states.add(target)

            if origin not in transictions:
                transictions[origin] = {}
            if letter not in transictions[origin]:
                transictions[origin][letter] = []
            transictions[origin][letter].append(target)

        return FiniteAutomaton(
            states, alphabet, transictions, initial_state, final_states
        )
