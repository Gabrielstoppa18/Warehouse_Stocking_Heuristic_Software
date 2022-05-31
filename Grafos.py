import igraph as ig
from igraph import plot

graph = {'A': ['B', 'C'],
          'B': ['A', 'C', 'D'],
          'C': ['A', 'B', 'D'],
          'D': ['B', 'C', 'F', 'G'],
          'E': ['F'],
          'F': ['D', 'E', 'H'],
          'G': ['D', 'H', 'I'],
          'H': ['F', 'G', 'I'],
          'I': ['G', 'H']}
def graph_plot(graph, x_box, y_box, color, layout_type):   
    # Instância Graph
    G = ig.Graph()

    # Separando chaves do dicionário
    graph_keys = list(graph.keys())

    # Adicionando n vértices no grafo
    G.add_vertices(len(graph_keys))

    # Encontrando índices das arestas e as adicionando no grafo
    graph_edges = []

    for i, key in enumerate(graph_keys):
        for j in graph[key]:
            if not (graph_keys.index(j), i) in graph_edges:
                graph_edges.append((i, graph_keys.index(j)))

    G.add_edges(graph_edges)

    # Plotagem do grafo
    box = (x_box, y_box)
    layout = G.layout(layout_type) # circle, drl, fr, kk, large, random, rt, rt_circular
    colors = [color] * len(graph_keys)
    return plot(G, layout=layout, bbox = box, vertex_label=graph_keys, vertex_color=colors)
graph_plot(graph, 300, 300, 'white', 'circle')    