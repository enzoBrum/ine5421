import os

from graphviz import Digraph


def desenhar_automato(nome, transicoes, start_state, end_states):
    # Garante que a pasta 'automatos/' exista
    pasta = "automatos"
    os.makedirs(pasta, exist_ok=True)

    if isinstance(end_states, str):
        end_states = {end_states}

    # Nome do arquivo final
    caminho_arquivo = os.path.join(pasta, f"automato_{nome}")

    # Cria o grafo
    dot = Digraph(format="png")
    dot.attr(rankdir="LR")  # Direção da esquerda para a direita
    dot.attr("node", shape="circle")

    dot.node("", shape="none")
    dot.edge("", start_state)

    for state in end_states:
        dot.node(state, shape="doublecircle")

    # Adiciona os nós e as arestas
    for estado_origem, trans in transicoes.items():
        for simbolo, destino in trans.items():
            if isinstance(destino, list):
                for d in destino:
                    dot.edge(estado_origem, d, label=simbolo)
            else:
                dot.edge(estado_origem, destino, label=simbolo)

    # Renderiza o grafo e salva o arquivo PNG na pasta especificada
    dot.render(caminho_arquivo, view=False)

