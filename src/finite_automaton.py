"""
Contém a classe utilizada para representar autômatos finitos.
"""

from copy import deepcopy

from generateAFN import ThompsonAFN

# Mapeia um estado à um dicionário cuja chave é uma letra do alfabeto e valor é a lista de
# estados alcançados quando se utiliza essa letra.
#
# e.g: transitions["0"] = {"a": ["0", "1"]} -> A partir do estado "0", é possível alcançar os estados "0" e "1" utilizando a letra "a"
Transictions = dict[str, dict[str, list[str]]]

# Símbolo usado para representar o vazio.
EPSILON = "&"


class FiniteAutomaton:
    """
    Classe representando um autômato finito.
    """

    states: set[str]
    alphabet: set[str]

    transitions: Transictions

    initial_state: str
    final_states: set[str]

    # Mapeia cada estado final à uma lista de possíveis
    # padrões à qual esse estado final pertence.
    #
    # e.g: id: [a-zA-Z]
    #      o estado final desse automato teria como pattern o `id`.
    final_states_to_pattern: dict[str, set[str]]

    def __init__(
        self,
        states: set[str],
        alphabet: set[str],
        transitions: Transictions,
        initial_state: str,
        final_states: str,
        final_states_to_pattern: dict[str, set[str]] = None,
    ):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states
        self.final_states_to_pattern = final_states_to_pattern

    @staticmethod
    def dumps(finite_automaton: "FiniteAutomaton") -> str:
        st_map = {state: i for i, state in enumerate(sorted(finite_automaton.states))}
        if finite_automaton.final_states_to_pattern:
            for st in finite_automaton.final_states:
                st_map[st] = f"{next(iter(finite_automaton.final_states_to_pattern[st]))}__q{st_map[st]}"


        final_st_map = {}
        ret = (
            f"{len(finite_automaton.states)}\n"
            f"{st_map[finite_automaton.initial_state]}\n"
            f"{','.join(str(x) for x in sorted(st_map[st] for st in finite_automaton.final_states))}\n"
            f"{','.join(sorted(finite_automaton.alphabet))}\n"
        )

        for origin_state, letter_dict in finite_automaton.transitions.items():
            for letter, target_states in letter_dict.items():
                for target in target_states:
                    ret += f"{st_map[origin_state]},{letter},{st_map[target]}\n"
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
        transitions: Transictions = {}
        states = set()
        final_states_to_pattern = {}
        
        for st in final_states:
            if "__" in st:
                final_states_to_pattern[st] = {st[:st.find("__")]}
            else:
                final_states_to_pattern[st] = {st}

        for line in lines[4:]:
            origin, letter, target = [x.strip() for x in line.split(",")]
            states.add(origin)
            states.add(target)

            if origin not in transitions:
                transitions[origin] = {}
            if letter not in transitions[origin]:
                transitions[origin][letter] = []
            transitions[origin][letter].append(target)
            
        for state in states:
            if state not in transitions:
                transitions[state] = {}

        return FiniteAutomaton(
            states, alphabet, transitions, initial_state, final_states, final_states_to_pattern
        )

    @staticmethod
    def from_thompson_afn(afn: ThompsonAFN) -> "FiniteAutomaton":
        start_state = afn.start
        final_states = {afn.final}
        states = {start_state, afn.final}
        alphabet = set()

        transitions: Transictions = deepcopy(afn.transitions)

        for state, letter_dict in transitions.items():
            states.add(state)
            for letter, val in letter_dict.items():
                alphabet.add(letter)
                if isinstance(val, str):
                    letter_dict[letter] = [val]

                for v in letter_dict[letter]:
                    states.add(v)

        for state in states:
            if state not in transitions:
                transitions[state] = {}

        return FiniteAutomaton(
            states, alphabet, transitions, start_state, final_states
        )

    @staticmethod
    def join_automatons(
        finite_automatons: dict[str, "FiniteAutomaton"],
    ) -> "FiniteAutomaton":
        new_states = {"q0"}
        start_state = "q0"
        final_states = set()
        new_transitions: Transictions = {"q0": {EPSILON: []}}
        new_alphabet = set()

        final_states_to_pattern: dict[str, set[str]] = {}

        for name, automaton in finite_automatons.items():
            state_map = {}
            new_alphabet |= automaton.alphabet

            for state in automaton.states:
                state_map[state] = f"q{len(new_states)}"
                new_states.add(state_map[state])
                new_transitions[state_map[state]] = {}

            final_states |= {state_map[state] for state in automaton.final_states}
            final_states_to_pattern |= {
                state_map[state]: {name} for state in automaton.final_states
            }

            for state, letter_dict in automaton.transitions.items():
                for letter, target_states in letter_dict.items():
                    if letter not in new_transitions[state_map[state]]:
                        new_transitions[state_map[state]][letter] = []
                    for target in target_states:
                        new_transitions[state_map[state]][letter].append(
                            state_map[target]
                        )

            new_transitions["q0"][EPSILON].append(state_map[automaton.initial_state])
        return FiniteAutomaton(
            new_states,
            new_alphabet,
            new_transitions,
            start_state,
            final_states,
            final_states_to_pattern,
        )
