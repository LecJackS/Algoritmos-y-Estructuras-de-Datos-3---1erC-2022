import teachmedijkstra

# initializing Directed graph
graph = teachmedijkstra.DirectedGraph()

# initializing vertices
graph.addVertex("a", (0, 2))
graph.addVertex("b", (1, 2))
graph.addVertex("c", (2, 2))
graph.addVertex("d", (0, 1))
graph.addVertex("e", (1, 1))
graph.addVertex("f", (2, 1))
graph.addVertex("g", (0, 0))
graph.addVertex("h", (1, 0))
graph.addVertex("i", (2, 0))

# adding edges
graph.addEdge("a", "b", 9)
graph.addEdge("b", "c", 3)
graph.addEdge("c", "f", 4)
graph.addEdge("e", "f", 3)
graph.addEdge("e", "d", 6)
graph.addEdge("d", "g", 1)
graph.addEdge("g", "h", 3)
graph.addEdge("h", "i", 8)
graph.addEdge("a", "d", 1)
graph.addEdge("e", "b", 3)
graph.addEdge("e", "h", 9)
graph.addEdge("f", "i", 6)
graph.addEdge("a", "e", 4)
graph.addEdge("c", "e", 5)
graph.addEdge("g", "e", 1)
graph.addEdge("i", "e", 4)
graph.addEdge("c", "i", 6)
graph.addEdge("a", "g", 1)


if __name__ == "__main__":
    # calling Dijkstra fnc to perform algo.
    dijkstra = teachmedijkstra.Dijkstra(graph, "a")
    dijkstra.run()


    # saving file
    dijkstra.saveToLaTeXFile("directedDij.tex")
