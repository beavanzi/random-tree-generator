from typing import List
import timeit
import random


# Beatriz Avanzi Ecli       RA 108612
# Sarah Anduca              RA 115506

class Vertice:
    def __init__(self, num: int) -> None:
        self.d = None
        self.f = None
        self.cor = None
        self.pai = None
        self.visited = False
        self.num = num
        self.adj: List[Vertice] = []


class Grafo:
    def __init__(self, n: int) -> None:
        self.vertices = [Vertice(i) for i in range(n)]
        self.numberOfVertices = n
        self.numberOfEdges = 0
        self.isConnected = True

    def addEdge(self, u: int, v: int):
        self.vertices[u].adj.append(self.vertices[v])
        self.vertices[v].adj.append(self.vertices[u])
        self.numberOfEdges = self.numberOfEdges + 1

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
    return graph


# Calculo do diameter
def Diameter(tree: Grafo) -> float:
    n: int = tree.pickRandomVertexId()  # pega um numero aleatorio no range da quantidade de vertices
    s: Vertice = tree.vertices[n]

    a: Vertice = tree.BFS(s)
    b: Vertice = tree.BFS(a)
    return b.d


def GenerateTXT(fileName, list):
    try:
        file = open(fileName, 'r+')
    except FileNotFoundError:
        file = open(fileName, 'w+')

    for sublist in list:
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
    assert graph1.isTree() == False

    # caso 2 - não é arvore, pois não é conexo
    graph2: Grafo = Grafo(5)
    graph2.addEdge(0, 1)
    graph2.addEdge(0, 2)
    graph2.addEdge(1, 3)
    graph2.addEdge(2, 1)
    assert graph2.isTree() == False

    # caso 3 - é arvore
    graph3: Grafo = Grafo(5)
    graph3.addEdge(0, 1)
    graph3.addEdge(0, 2)
    graph3.addEdge(1, 3)
    graph3.addEdge(2, 4)
    assert graph3.isTree() == True


def TEST_RandomTreeRandomWalk():
    for i in range(500):
        graph250: Grafo = RandomTreeRandomWalk(250)
        graph500: Grafo = RandomTreeRandomWalk(500)
        graph750: Grafo = RandomTreeRandomWalk(750)
        graph1000: Grafo = RandomTreeRandomWalk(1000)
        graph1250: Grafo = RandomTreeRandomWalk(1250)
        graph1500: Grafo = RandomTreeRandomWalk(1500)
        graph1750: Grafo = RandomTreeRandomWalk(1750)
        graph2000: Grafo = RandomTreeRandomWalk(2000)
        assert graph250.isTree()
        assert graph500.isTree()
        assert graph750.isTree()
        assert graph1000.isTree()
        assert graph1250.isTree()
        assert graph1500.isTree()
        assert graph1750.isTree()
        assert graph2000.isTree()


def RunAllTests():
    TEST_Diameter()
    TEST_isTree()
    TEST_RandomTreeRandomWalk()


def RunRandomWalk():
    random_walk_result = []
    entries = [250, 500, 750, 1000, 1250, 1500, 1750, 2000]
    for entry in entries:
        diameterSum = 0
        n = 100
        for i in range(n):
            tree = RandomTreeRandomWalk(entry)
            diameter = Diameter(tree)
            diameterSum = diameter + diameterSum
        diameterAvg = diameterSum / n
        random_walk_result.append([entry, diameterAvg])

    GenerateTXT("randomwalk.txt", random_walk_result)


def main():
    inicio = timeit.default_timer()

    RunRandomWalk()
    RunAllTests()

    fim = timeit.default_timer()

    # mostra o tempo que demorou para execução
    print('Calculo da duracao: %f' % (fim - inicio))


if __name__ == '__main__':
    main()
