from typing import List
import timeit
import random
from copy import deepcopy
from operator import itemgetter


# Beatriz Avanzi Ecli       RA 108612
# Sarah Anduca              RA 115506

class DisjointSets:
    parent = {}
    rank = {}

    def MakeSet(self, vertex):
        self.parent[vertex] = vertex
        self.rank[vertex] = 0

    def FindSet(self, vertex):
        if self.parent[vertex] == vertex:
            return vertex
        return self.FindSet(self.parent[vertex])

    def Union(self, vertex_u, vertex_v):
        vertex_u_root = self.FindSet(vertex_u)
        vertex_v_root = self.FindSet(vertex_v)

        if self.rank[vertex_u_root] > self.rank[vertex_v_root]:
            self.parent[vertex_v_root] = vertex_u_root
        elif self.rank[vertex_u_root] < self.rank[vertex_v_root]:
            self.parent[vertex_u_root] = vertex_v_root
        else:
            self.parent[vertex_u_root] = vertex_v_root
            self.rank[vertex_v_root] += 1


class Vertice:
    def __init__(self, num: int) -> None:
        self.d = None
        self.f = None
        self.cor = None
        self.pai = None
        self.visited = False
        self.num = num
        self.adj: List[Vertice] = []


class Edge:
    weight: float
    u: int
    v: int

    def __init__(self, u: int, v: int) -> None:
        self.weight = 0
        self.u = u
        self.v = v


class Grafo:
    numberOfVertices: int
    numberOfEdges: int
    edgesWeight: List[float]

    def __init__(self, n: int) -> None:
        self.vertices = [Vertice(i) for i in range(n)]
        self.edges = []
        self.numberOfVertices = n
        self.numberOfEdges = 0
        self.isConnected = True
        self.edgesWeight: dict = {}

    def addEdge(self, u: int, v: int):
        self.vertices[u].adj.append(self.vertices[v])
        self.vertices[v].adj.append(self.vertices[u])
        self.numberOfEdges = self.numberOfEdges + 1
        self.edges.append(Edge(u, v))

    # Pega o "id" de um vertice aleatorio do grafo
    def pickRandomVertexId(self) -> int:
        n: int = random.randrange(len(self.vertices))
        return n

    # Inicialização dos vertices
    def initializeAllVertex(self):
        for v in self.vertices:
            v.d = -1
            v.pai = None
            v.cor = "branco"
            v.f = -1

    # BFS que retorna o ultimo vertice dequeued
    def BFS(self, s: Vertice):
        self.initializeAllVertex()
        s.d = 0
        s.cor = "cinza"
        Q = [s]
        u = None

        while Q:
            u = Q.pop(0)
            for v in self.vertices[u.num].adj:
                if v.cor == "branco":
                    v.cor = "cinza"
                    v.d = u.d + 1
                    v.pai = u
                    Q.append(v)
            u.cor = "preto"

        return u

    # Verifica se é uma arvore
    def isTree(self):
        # ve se arestas = vertices - 1
        if not self.numberOfEdges == self.numberOfVertices - 1:
            return False

        # ve se é conexo
        x: int = self.pickRandomVertexId()
        s: Vertice = self.vertices[x]

        self.BFS(s)

        self.isConnected = True

        for v in self.vertices:
            if v.cor == "branco":
                self.isConnected = False

        if self.isConnected:
            return True

        return False


def GenerateFullGraph(n: int) -> Grafo:
    graph: Grafo = Grafo(n)
    fullGraphNumberEdges = (n * (n - 1)) / 2
    verticesAvailable = deepcopy(graph.vertices)
    verticesAvailable.pop(0)
    for vertexIndex in range(graph.numberOfVertices - 1):
        for accessibleVertex in verticesAvailable:
            graph.addEdge(vertexIndex, accessibleVertex.num)
        assert len(graph.vertices[vertexIndex].adj) == n-1
        verticesAvailable.pop(0)

    assert graph.numberOfEdges == fullGraphNumberEdges
    return graph


# Geração de arvore aleatoria pelo algoritmo de Kruskal
def RandomTreeKruskal(n: int) -> Grafo:
    graph: Grafo = GenerateFullGraph(n)

    for edge in graph.edges:
        weight = random.random()
        edge.weight = weight
        graph.edgesWeight[weight] = edge
    MST_Kruskal(graph)

    # assert graph.isTree()
    return graph


def MST_Kruskal(graph: Grafo):
    # tree: Grafo = Grafo(graph.numberOfVertices)
    treeGroup = []
    disjointSets = DisjointSets()
    for vertex in graph.vertices:
        disjointSets.MakeSet(vertex)
    edgesSorted: dict = sorted(graph.edgesWeight.items(), key=itemgetter(0))
    for (weight, edge) in edgesSorted:
        if disjointSets.FindSet(edge.u) != disjointSets.FindSet(edge.v):
            # tree.addEdge(u, v)
            treeGroup.append(edge)
            disjointSets.Union(edge.u, edge.v)

    return treeGroup


# Geração de arvore aleatoria
def RandomTreeRandomWalk(n: int) -> Grafo:
    graph: Grafo = Grafo(n)
    for u in graph.vertices:
        u.visited = False

    x: int = graph.pickRandomVertexId()
    u: Vertice = graph.vertices[x]
    u.visited = True
    while graph.numberOfEdges < n - 1:
        y: int = graph.pickRandomVertexId()
        v: Vertice = graph.vertices[y]
        if not v.visited:
            graph.addEdge(u.num, v.num)
            v.visited = True
        u = v

    assert graph.isTree()
    return graph


# Calculo do diameter
def Diameter(tree: Grafo) -> float:
    n: int = tree.pickRandomVertexId()  # pega um numero aleatorio no range da quantidade de vertices
    s: Vertice = tree.vertices[n]

    a: Vertice = tree.BFS(s)
    b: Vertice = tree.BFS(a)
    return b.d


def GenerateTXT(fileName: str, elements):
    try:
        file = open(fileName, 'r+')
    except FileNotFoundError:
        file = open(fileName, 'w+')

    for sublist in elements:
        file.write(str(sublist[0]) + " " + str(sublist[1]) + "\n")

    file.close()


def TEST_Diameter():
    graph1: Grafo = Grafo(4)
    graph1.addEdge(0, 1)
    graph1.addEdge(2, 1)
    graph1.addEdge(3, 1)
    assert Diameter(graph1) == 2

    graph2: Grafo = Grafo(9)
    graph2.addEdge(0, 1)
    graph2.addEdge(0, 2)
    graph2.addEdge(2, 3)
    graph2.addEdge(2, 8)
    graph2.addEdge(3, 6)
    graph2.addEdge(3, 4)
    graph2.addEdge(4, 5)
    graph2.addEdge(5, 7)
    assert Diameter(graph2) == 6


def TEST_isTree():
    # caso 1 - não é arvore, pois arestas != vertices - 1

    graph1: Grafo = Grafo(5)
    graph1.addEdge(0, 1)
    graph1.addEdge(2, 1)
    graph1.addEdge(3, 1)
    assert not graph1.isTree()

    # caso 2 - não é arvore, pois não é conexo
    graph2: Grafo = Grafo(5)
    graph2.addEdge(0, 1)
    graph2.addEdge(0, 2)
    graph2.addEdge(1, 3)
    graph2.addEdge(2, 1)
    assert not graph2.isTree()

    # caso 3 - é arvore
    graph3: Grafo = Grafo(5)
    graph3.addEdge(0, 1)
    graph3.addEdge(0, 2)
    graph3.addEdge(1, 3)
    graph3.addEdge(2, 4)
    assert graph3.isTree()


def RunAllTests():
    TEST_Diameter()
    TEST_isTree()


def RunRandomWalk():
    random_walk_result = []
    entries = [250, 500, 750, 1000, 1250, 1500, 1750, 2000]
    for entry in entries:
        diameterSum = 0
        n = 500
        for i in range(n):
            tree = RandomTreeRandomWalk(entry)
            diameter = Diameter(tree)
            diameterSum = diameter + diameterSum

        diameterAvg = diameterSum / n
        random_walk_result.append([entry, diameterAvg])

    GenerateTXT("randomwalk.txt", random_walk_result)


def main():
    inicio = timeit.default_timer()

    # RunRandomWalk()
    # RunAllTests()
    RandomTreeKruskal(4)

    fim = timeit.default_timer()

    # mostra o tempo que demorou para execução
    print('Calculo da duracao: %f' % (fim - inicio))


if __name__ == '__main__':
    main()
