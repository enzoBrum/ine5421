def item_in_list(item, items):
    for existing in items:
        if existing[0] == item[0] and existing[1] == item[1] and existing[2] == item[2]:
            return True
    return False

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

def go_to(items, symbol, productions):
    moved_items = []
    for lhs, rhs, dot_pos in items:
        if dot_pos < len(rhs) and rhs[dot_pos] == symbol:
            new_item = (lhs, rhs, dot_pos + 1)
            if not item_in_list(new_item, moved_items):
                moved_items.append(new_item)
    return closure(moved_items, productions)

# Verifica se dois estados (listas de itens) são iguais
def estados_iguais(e1, e2):
    if len(e1) != len(e2):
        return False
    for item in e1:
        if not item_in_list(item, e2):
            return False
    return True

# Verifica se um estado já existe na lista
def estado_em_lista(estado, lista_estados):
    for i, e in enumerate(lista_estados):
        if estados_iguais(estado, e):
            return i  # retorna índice
    return -1

def build_canonical_collection(estados, productions):
    transicoes  = []

    i = 0
    while i < len(estados):
        estado_atual = estados[i]

        # Só coleta os símbolos após o ponto (·), na ordem de ocorrência
        simbolos_uteis = []
        for lhs, rhs, dot in estado_atual:
            if dot < len(rhs):
                simbolo = rhs[dot]
                if simbolo not in simbolos_uteis:
                    simbolos_uteis.append(simbolo)

        # Aplica go_to apenas nos símbolos que realmente aparecem no estado
        for simbolo in simbolos_uteis:
            novo_estado = go_to(estado_atual, simbolo, productions)
            if novo_estado:
                indice_existente = estado_em_lista(novo_estado, estados)
                if indice_existente == -1:
                    estados.append(novo_estado)
                    indice_existente = len(estados) - 1
                transicoes.append((i, simbolo, indice_existente))
        i += 1
    return estados
