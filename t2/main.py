# main.py

from utils import closure, go_to, estado_em_lista

# Produções originais
productions = {
    'E': [['E', '+', 'T'], ['T']],
    'T': [['T', '*', 'F'], ['F']],
    'F': [['(', 'E', ')'], ['id']]
}

# Inicializa estados com closure do item inicial
item_inicial = ("E'", ['E'], 0)
estados = [closure([item_inicial], productions)]
transicoes = []

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

# Exibe os estados
for idx, estado in enumerate(estados):
    print(f"\nEstado {idx}:")
    for item in estado:
        lhs, rhs, dot = item
        antes = ' '.join(rhs[:dot])
        depois = ' '.join(rhs[dot:])
        print(f"  {lhs} → {antes} · {depois}")
