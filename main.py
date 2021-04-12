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

    # BFS
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


# Retorna o ultimo vertice de um grafo
def GetLastVertex(graph: Grafo) -> Vertice:
    v: Vertice = graph.vertices[len(graph.vertices)]
    return v


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
def Diameter(tree: Grafo) -> int:
    n: int = tree.pickRandomVertexId()  # pega um numero aleatorio no range da quantidade de vertices
    s: Vertice = tree.vertices[n]

    tree.BFS(s)
    a: Vertice = GetLastVertex(tree)
    tree.BFS(a)
    b: Vertice = GetLastVertex(tree)
    return b.d


def TEST_RandomTreeRandomWalk():
    for i in range(1000):
        print('Suit - RandomTreeRandomWalk: ', i)
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


def main():
    inicio = timeit.default_timer()

    TEST_RandomTreeRandomWalk()

    fim = timeit.default_timer()

    # mostra o tempo que demorou para execução
    print('Calculo da duracao: %f' % (fim - inicio))


if __name__ == '__main__':
    main()
