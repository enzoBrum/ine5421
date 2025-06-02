from collections import deque

from finite_automaton import EPSILON, FiniteAutomaton, Transictions


def find_epsilon_closures(automaton: FiniteAutomaton) -> dict[str, set[str]]:
    """
    Acha o epsilon fecho do estado desejado.
    """

    queue = deque([automaton.initial_state])
    reachable = {automaton.initial_state}

    epsilon_closure = {}

    while len(queue) > 0:
        cur = queue.pop()

        for states in automaton.transitions[cur].values():
            for state in states:
                if state not in reachable:
                    reachable.add(state)
                    queue.appendleft(state)

    for state in reachable:
        queue = deque([state])

        closure = {state}
        while len(queue) > 0:
            cur = queue.pop()

            if EPSILON not in automaton.transitions[cur]:
                continue

            for st in automaton.transitions[cur][EPSILON]:
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

    new_transitions: Transictions = {}
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

        transitions: dict[str, set[str]] = {}
        for state in cur_states:
            if state in automaton.final_states:
                final_states.add(formatted_states)
                
                if automaton.final_states_to_pattern is not None:
                    if formatted_states not in final_states_to_pattern:
                        final_states_to_pattern[formatted_states] = set()
                        final_states_to_pattern[
                            formatted_states
                        ] |= automaton.final_states_to_pattern[state]

            for letter in automaton.transitions[state]:
                if letter == EPSILON:
                    continue

                if letter not in transitions:
                    transitions[letter] = set()

                for other_state in automaton.transitions[state][letter]:
                    transitions[letter] |= epsilon_closure[other_state]

        new_transitions[formatted_states] = {}
        for letter in transitions:
            formatted_target_states = format_states(transitions[letter])

            new_transitions[formatted_states][letter] = [formatted_target_states]
            st.append(transitions[letter])

    return FiniteAutomaton(
        new_states,
        automaton.alphabet - {EPSILON},
        new_transitions,
        initial_state,
        final_states,
        final_states_to_pattern,
    )

