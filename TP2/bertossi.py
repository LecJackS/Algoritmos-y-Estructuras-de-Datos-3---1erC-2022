import pandas as pd
import teachmedijkstra
import networkx as nx

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


import graphviz


def overlap(x, y):
    return (x[0] <= y[0] <= x[1]) or (y[0] <= x[0] <= y[1])

def categorizar_aristas(nodos):
    B = [] # Intersecan
    C = [] # Disjuntos

    for i, x in enumerate(nodos):
        for j, y in enumerate(nodos):
            if i < j:
                if overlap(x,y):
                    # H: x[0] < y[0]
                    B.append((i+1, j+1))  # Indice arranca en 1, no cero
                else:
                    C.append((i+1, j+1))  # Indice arranca en 1, no cero

    return B, C

def generar_dummies(nodos):
    min_val = 0
    max_val = 9 # TODO: Funcion que busque min y max entre los nodos
    #inicio = pd.Interval(min_val-2, min_val-1, closed='both')
    #fin    = pd.Interval(max_val+1, max_val+2, closed='both')
    int_dum_inicio = (min_val - 2, min_val - 1)
    int_dum_fin    = (max_val + 1, max_val + 2)

    aristas_dum_inicio = []
    aristas_dum_fin = []
    m = len(nodos) + 1
    for j, y in enumerate(nodos):
        aristas_dum_inicio.append((0, j+1))
        aristas_dum_fin.append((j+1, m))

    return int_dum_inicio, int_dum_fin, aristas_dum_inicio, aristas_dum_fin


if __name__ == "__main__":
    n = 5
    # initializing Directed graph
    graph = teachmedijkstra.DirectedGraph()
    G = graphviz.Digraph('D prima', comment='Grafo temporal para calcular CDT')

    # TODO: Los ordeno por primer elemento!!! Ahora asumo que estan ordenados.
    # nodos = [pd.Interval(0, 6, closed='both'),
    #          pd.Interval(1, 3, closed='both'),
    #          pd.Interval(2, 4, closed='both'),
    #          pd.Interval(5, 8, closed='both'),
    #          pd.Interval(7, 9, closed='both')
    #          ]

    nodos = [(0, 6),
             (1, 3),
             (2, 4),
             (5, 8),
             (7, 9)
             ]

    val_dum_inicio, val_dum_fin, aristas_dum_inicio, aristas_dum_fin = generar_dummies(nodos)

    m = len(nodos) + 1
    graph.addVertex("0", (-4, -m//2 + 0.5))
    G.node("0", shape="egg", color="green", penwidth="3")
    for i, nodo in enumerate(nodos):
        # initializing vertices
        graph.addVertex(str(i + 1) + "in", (-2, -(i + 1)))
        graph.addVertex(str(i + 1) + "out", (2, -(i + 1)))
        G.node(str(i + 1) + "in", "[{},{}]_in".format(nodo[0], nodo[1]), shape="rectangle", color="blue")
        G.node(str(i + 1) + "out", "[{},{}]_out".format(nodo[0], nodo[1]), shape="rectangle", color="red")


    graph.addVertex(str(m), (4, -m//2 + 0.5))
    G.node(str(m), shape="egg", color="green", penwidth="3")



    B, C = categorizar_aristas(nodos)

    print(B)
    print(C)

    Dprima = {}

    # To see this, we define another directed network D' by splitting each node i, i in [1, n], into two nodes, say i_in and i_out.
    # These two nodes are joined by the arc (i_in, i_out) , whose length is zero.
    for i, (x, y) in enumerate(nodos):
        c = (x + y) // 2
        assert (c is not x) and (c is not y), "Se rompio todo por dividir por dos algo muy chico"

        Dprima[((i+1, 'in'), (i+1, 'out'))] = 0

    for (i, j) in B:
        # Intervalos que comparten valores (nodos conectados en el grafo original)
        Dprima[((i, 'out'), (j, 'in'))] = 1

    for (i, j) in C:
        # Intervalos disjuntos (nodos NO conectados en el grafo original)
        Dprima[((i, 'in'), (j, 'out'))] = 1

    for i, (x, y) in enumerate(aristas_dum_inicio):
        # Intervalos disjuntos (nodos NO conectados en el grafo original)
        Dprima[((0, ''), (i+1, 'out'))] = 1


    for i, (x, y) in enumerate(aristas_dum_fin):
        # Intervalos disjuntos (nodos NO conectados en el grafo original)
        Dprima[((i+1, 'in'), (m, ''))] = 1


    print(Dprima)
    for k, v in Dprima.items():
        #print("los que agrego")
        #print((str(k[0][0])+str(k[0][1]), str(k[1][0])+str(k[1][1]), v))
        graph.addEdge(str(k[0][0])+str(k[0][1]), str(k[1][0])+str(k[1][1]), v)
        G.edge(str(k[0][0])+str(k[0][1]), str(k[1][0])+str(k[1][1]), weight=str(v), color=['red', 'black'][v])
        #G.edges[(str(k[0][0])+str(k[0][1]), str(k[1][0])+str(k[1][1]))]["weight"] = v

    print(G.source)

    G.view()
    #p = nx.shortest_path(G, source="0", target=str(m))
    #print(p)
    #dijkstra = teachmedijkstra.Dijkstra(graph, "0")

    #dijkstra.show()

    #print(dijkstra.exportTableToText())
    #dijkstra.saveToLaTeXFile("bertossidijsktra.tex")
    #dijkstra.run()
    # saving file
    #dijkstra.saveToLaTeXFile("bertossidijsktrasolved.tex")
    # 0 1 2 3 4 5 6
    #   1 2 3
    #     2 3 4
    #           5 6 7 8
    #               7 8 9

