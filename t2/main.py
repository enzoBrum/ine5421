# main.py

from utils import build_canonical_collection, closure, go_to, estado_em_lista

# Produções originais
productions = {
    'E': [['E', '+', 'T'], ['T']],
    'T': [['T', '*', 'F'], ['F']],
    'F': [['(', 'E', ')'], ['id']]
}

# Inicializa estados com closure do item inicial
item_inicial = ("E'", ['E'], 0)
estados = [closure([item_inicial], productions)]
estados = build_canonical_collection(estados, productions)

# Exibe os estados
for idx, estado in enumerate(estados):
    print(f"\nEstado {idx:3}:")
    for item in estado:
        lhs, rhs, dot = item
        antes = ' '.join(rhs[:dot])
        depois = ' '.join(rhs[dot:])
        print(f"  {lhs:3} → {antes} · {depois}")
