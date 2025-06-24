# Produções no formato fornecido
productions = {
    'S': ['SvA', 'A'],
    'A': ['AˆB', 'B'],
    'B': ['nB', '(S)', 't', 'f']
}

# Converter produções para listas de símbolos
for key in productions:
    productions[key] = [list(p) for p in productions[key]]

# Função que verifica se um item já está na lista (evita duplicatas)
def item_in_list(item, items):
    for existing in items:
        if existing[0] == item[0] and existing[1] == item[1] and existing[2] == item[2]:
            return True
    return False

# Função que calcula o closure
def closure(items, productions):
    closure_items = items.copy()

    i = 0
    while i < len(closure_items):
        lhs, rhs, dot_pos = closure_items[i]

        if dot_pos < len(rhs):
            symbol = rhs[dot_pos]
            if symbol in productions:
                for prod in productions[symbol]:
                    new_item = (symbol, prod, 0)
                    if not item_in_list(new_item, closure_items):
                        closure_items.append(new_item)
        i += 1

    return closure_items

# Exemplo de uso: item inicial é S' → ·S
start_item = ("S'", ['S'], 0)

# Calcula closure
resultado = closure([start_item], productions)

# Exibe os itens resultantes
for item in resultado:
    lhs, rhs, dot_pos = item
    antes_ponto = ''.join(rhs[:dot_pos])
    depois_ponto = ''.join(rhs[dot_pos:])
    print(f"{lhs} → {antes_ponto}·{depois_ponto}")
