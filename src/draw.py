import os
from graphviz import Digraph

def desenhar_automato(nome, transicoes):
    # Garante que a pasta 'automatos/' exista
    pasta = 'automatos'
    os.makedirs(pasta, exist_ok=True)

    # Nome do arquivo final
    caminho_arquivo = os.path.join(pasta, f'automato_{nome}')

    # Cria o grafo
    dot = Digraph(format='png')
    dot.attr(rankdir='LR')  # Direção da esquerda para a direita
    dot.attr('node', shape='circle')

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