from collections import deque

from finite_automaton import EPSILON, FiniteAutomaton, Transictions


def find_epsilon_closures(automaton: FiniteAutomaton) -> dict[str, set[str]]:
    """
    Acha o epsilon fecho do estado desejado.

    O(V^3).

    Poderia ser melhor com heurísticas como https://cp-algorithms.com/graph/strongly-connected-components.html ou
    só usando uma BFS (em grafos onde há vários estados inalcançáveis)
    """

    queue = deque([automaton.initial_state])
    reachable = {automaton.initial_state}

    epsilon_closure = {}

    while len(queue) > 0:
        cur = queue.pop()

        for states in automaton.transictions[cur].values():
            for state in states:
                if state not in reachable:
                    reachable.add(state)
                    queue.appendleft(state)

    for state in reachable:
        queue = deque([state])

        closure = {state}
        while len(queue) > 0:
            cur = queue.pop()

            if EPSILON not in automaton.transictions[cur]:
                continue

            for st in automaton.transictions[cur][EPSILON]:
                if st in closure:
                    continue
                closure.add(st)
                queue.append(st)

        epsilon_closure[state] = closure

    return epsilon_closure


def format_states(states: set[str]) -> str:
    return f"{{{','.join(sorted(states))}}}"


def determinize(
    automaton: FiniteAutomaton,
) -> FiniteAutomaton:
    """
    Realiza a determinização do autômato.
    """

    new_transictions: Transictions = {}
    new_states = set()

    epsilon_closure = find_epsilon_closures(automaton)

    st = [epsilon_closure[automaton.initial_state]]
    initial_state = format_states(epsilon_closure[automaton.initial_state])
    final_states = set()
    final_states_to_pattern: dict[str, list[str]] = {}

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
                if (
                    formatted_states not in final_states_to_pattern
                    and automaton.final_states_to_pattern is not None
                ):
                    final_states_to_pattern[formatted_states] = set()
                final_states_to_pattern[
                    formatted_states
                ] |= automaton.final_states_to_pattern[state]

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
        new_states,
        automaton.alphabet - {EPSILON},
        new_transictions,
        initial_state,
        final_states,
        final_states_to_pattern,
    )


if __name__ == "__main__":
    from sys import stdin

    # automaton = FiniteAutomaton.loads(stdin.read())
    with open("/home/erb/ufsc/INE5421/src/input") as f:
        automaton = FiniteAutomaton.loads(f.read())
    print(FiniteAutomaton.dumps(determinize(automaton)))
