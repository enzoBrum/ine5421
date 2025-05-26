from re import L
from finite_automaton import EPSILON, FiniteAutomaton, Transictions


def find_epsilon_closures(automaton: FiniteAutomaton) -> dict[str, set[str]]:
    """
    Acha o epsilon fecho do estado desejado.

    O(V^3).

    Poderia ser melhor com heurísticas como https://cp-algorithms.com/graph/strongly-connected-components.html ou
    só usando uma BFS (em grafos onde há vários estados inalcançáveis)
    """

    dist_matrix = [
        [False for _ in range(len(automaton.states))]
        for _ in range(len(automaton.states))
    ]

    states = list(automaton.states)
    state_to_idx = {state: i for i, state in enumerate(states)}

    for u in automaton.states:
        dist_matrix[state_to_idx[u]][state_to_idx[u]] = True
        for v in automaton.transictions[u].get(EPSILON, []):
            dist_matrix[state_to_idx[u]][state_to_idx[v]] = True

    dp = [
        [False for _ in range(len(automaton.states))]
        for _ in range(len(automaton.states))
    ]
    for u in automaton.states:
        dp[state_to_idx[u]][state_to_idx[u]] = True

    for k in range(len(automaton.states)):
        for u in range(len(automaton.states)):
            for v in range(len(automaton.states)):
                dp[u][v] = dp[u][v] or (dist_matrix[u][k] and dist_matrix[k][v])

    epsilon_closure: dict[str, set[str]] = {state: set() for state in automaton.states}
    for u in range(len(automaton.states)):
        for v in range(len(automaton.states)):
            if dp[u][v]:
                epsilon_closure[states[u]].add(states[v])
    return epsilon_closure


def format_states(states: set[str]) -> str:
    return f"{{{','.join(sorted(states))}}}"


def determinize(automaton: FiniteAutomaton) -> FiniteAutomaton:
    """
    Realiza a determinização do autômato.
    """

    new_transictions: Transictions = {}
    new_states = set()

    epsilon_closure = find_epsilon_closures(automaton)

    st = [epsilon_closure[automaton.initial_state]]
    initial_state = format_states(epsilon_closure[automaton.initial_state])
    final_states = set()

    while len(st) > 0:
        cur_states = st.pop()

        formatted_states = format_states(cur_states)

        if formatted_states in new_states:
            continue
        new_states.add(formatted_states)

        transictions: dict[str, set[str]] = {}
        for state in cur_states:
            if state in automaton.final_states:
                final_states.add(formatted_states)

            for letter in automaton.transictions[state]:
                if letter == EPSILON:
                    continue

                if letter not in transictions:
                    transictions[letter] = set()

                for other_state in automaton.transictions[state][letter]:
                    transictions[letter] |= epsilon_closure[other_state]

        new_transictions[formatted_states] = {}
        for letter in transictions:
            formatted_target_states = format_states(transictions[letter])

            new_transictions[formatted_states][letter] = [formatted_target_states]
            st.append(transictions[letter])

    return FiniteAutomaton(
        new_states, automaton.alphabet, new_transictions, initial_state, final_states
    )


if __name__ == "__main__":
    from sys import stdin

    # automaton = FiniteAutomaton.loads(stdin.read())
    with open("/home/erb/ufsc/INE5421/src/input") as f:
        automaton = FiniteAutomaton.loads(f.read())
    print(FiniteAutomaton.dumps(determinize(automaton)))
