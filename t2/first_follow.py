from collections import defaultdict


def tokenize_production(production):
    production = production.replace(' ', '')
    tokens = []
    i = 0
    while i < len(production):
        c = production[i]

        # Skip whitespace
        if c.isspace():
            i += 1
            continue

        # Special operator ::= (must come before ':' or '=')
        if production[i:i+3] == '::=':
            tokens.append('::=')
            i += 3

        # One-character terminal symbols
        elif c in '()+-=*;,':  # add/remove symbols as needed
            tokens.append(c)
            i += 1

        # Terminal: lowercase sequences [a-z]+
        elif c.islower():
            start = i
            while i < len(production) and production[i].islower():
                i += 1
            tokens.append(production[start:i])

        # Non-terminal: Uppercase identifier (e.g., E, T, Expr)
        elif c.isupper():
            start = i
            while i < len(production) and (production[i].isalnum() or production[i] == '_'):
                i += 1
            tokens.append(production[start:i])

        # Epsilon or placeholder
        elif c == '#':
            tokens.append('#')
            i += 1

        else:
            raise ValueError(f"Unexpected character: {c}")

    return tokens


def compute_first(symbol: str, first_sets: dict[str, set[str]], terminal_symbols: set[str], productions: dict[str, list[list[str]]], visited: set[str]) -> set[str]:
    if symbol in terminal_symbols or symbol in '()':
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
                first = compute_first(char, first_sets, terminal_symbols, productions, visited.copy())
                result |= (first - {'#'})
                if '#' not in first:
                    break
            else:
                result.add('#')

    first_sets[symbol] = result
    return result

def compute_follow(symbol: str, start_symbol: str, first_sets: dict[str, set[str]], follow_sets: dict[str, set[str]], productions: dict[str, list[list[str]]], terminal_symbols: set[str],  visited: set[str]) -> set[str]:
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
                            b_first = compute_first(b, first_sets, terminal_symbols, productions, visited)
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
                                follow_sets[symbol] |= compute_follow(A, start_symbol, first_sets, follow_sets, productions, terminal_symbols, visited.copy())

                    else:
                        # Regra 3: B está no fim → FOLLOW(A) ⊆ FOLLOW(B)
                        if A != symbol:
                            follow_sets[symbol] |= compute_follow(A, start_symbol, first_sets, follow_sets, productions, terminal_symbols, visited.copy())

    return follow_sets[symbol]


if __name__ == "__main__":
    productions = {}
    
    with open('input_grammar.txt', 'r') as file:
        for line in file:
            if not line.strip():
                continue
            lhs, rhs = line.strip().split('::=')
            lhs = lhs.strip()
            rhs_alternatives = rhs.strip().split('|')
            rhs_parsed = [tokenize_production(alt.strip()) for alt in rhs_alternatives]
            productions[lhs] = rhs_parsed

    '''
    productions = {
        
        'E': [['E', '+', 'T'], ['T']],
        'T': [['T', '*', 'F'], ['F']],
        'F': [['(', 'E', ')'], ['id']]

    }
    '''

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


    # Compute FIRST sets
    print("FIRST sets:")
    visited = set()
    for nt in non_terminals:
        first = compute_first(nt, first_sets, terminals, productions, visited)
        print(f"First({nt}) = {{ {', '.join(sorted(first))} }}")

    print("\nFOLLOW sets:")
    visited = set()
    for nt in non_terminals:
        follow = compute_follow(nt, start_symbol, first_sets, follow_sets, productions, terminals, visited)
        print(f"Follow({nt}) = {{ {', '.join(sorted(follow))} }}")
