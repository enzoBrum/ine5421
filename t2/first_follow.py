from collections import defaultdict

productions = {
    'S': ['SvA', 'A'],
    'A': ['AˆB', 'B'],
    'B': ['nB', '(S)', 't', 'f']
}

start_symbol = next(iter(productions)) # Get the start symbol dynamically

non_terminals = list(productions.keys())
terminals = set()
first_sets = defaultdict(set)
follow_sets = defaultdict(set)

# Collect all terminals
for rules in productions.values():
    for rule in rules:
        for char in rule:
            if not char.isupper() and char not in '()#':
                terminals.add(char)

def compute_first(symbol, visited=set()):
    if symbol in terminals or symbol in '()':
        return {symbol}
    if symbol == '#':
        return {'#'}
    if symbol in visited:
        return set()  # prevent infinite recursion

    if first_sets[symbol]:
        return first_sets[symbol]

    visited.add(symbol)
    result = set()

    for rule in productions.get(symbol, []):
        if rule == '#':
            result.add('#')
        else:
            for i, char in enumerate(rule):
                first = compute_first(char, visited.copy())
                result |= (first - {'#'})
                if '#' not in first:
                    break
            else:
                result.add('#')

    first_sets[symbol] = result
    return result

def compute_follow(symbol, visited=set()):
    if symbol in visited:
        return follow_sets[symbol]

    visited.add(symbol)
    if symbol == start_symbol:  # start symbol
        follow_sets[symbol].add('$')

    for A, rules in productions.items():
        for rule in rules:
            for idx, B in enumerate(rule):
                if B == symbol:
                    beta = rule[idx+1:]

                    if beta:
                        # FIRST(β)
                        beta_first = set()
                        for b in beta:
                            b_first = compute_first(b)
                            beta_first |= (b_first - {'#'})
                            if '#' in b_first:
                                continue
                            else:
                                break
                        else:
                            beta_first.add('#')

                        follow_sets[symbol] |= (beta_first - {'#'})

                        # Regra 3: Se ε ∈ FIRST(β), adicione FOLLOW(A) em FOLLOW(B)
                        if '#' in beta_first:
                            if A != symbol:
                                follow_sets[symbol] |= compute_follow(A, visited.copy())

                    else:
                        # Regra 3: B está no fim → FOLLOW(A) ⊆ FOLLOW(B)
                        if A != symbol:
                            follow_sets[symbol] |= compute_follow(A, visited.copy())

    return follow_sets[symbol]


# Compute FIRST sets
print("FIRST sets:")
for nt in non_terminals:
    first = compute_first(nt)
    print(f"First({nt}) = {{ {', '.join(sorted(first))} }}")

print("\nFOLLOW sets:")
for nt in non_terminals:
    follow = compute_follow(nt)
    print(f"Follow({nt}) = {{ {', '.join(sorted(follow))} }}")
