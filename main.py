from typing import List
import time
import timeit

fileTreeName = "arvore-0"

class Vertice:
    def __init__(self, num: int) -> None:
        self.d = None
        self.cor = None
        self.pai = None
        self.adj = None
        self.num = num
        self.adj: List[Vertice] = []


class Grafo:
    def __init__(self, n: int) -> None:
        self.vertices = [Vertice(i) for i in range(n)]
        self.numberOfVertices = n
        self.diameterAssertion = None

    def addAresta(self, u: int, v: int):
        self.vertices[u].adj.append(self.vertices[v])
        self.vertices[v].adj.append(self.vertices[u])


def InitializeAllVertex(T: Grafo) -> Grafo:
    for v in T.vertices:
        v.d = -1
        v.pai = None
        v.cor = "branco"
    return T


def LongestPathBFS(T: Grafo, s: Vertice) -> Vertice:
    T: Grafo = InitializeAllVertex(T)
    s.d = 0
    s.cor = "cinza"
    Q = [s]
    u = None

    while Q:
        u = Q.pop(0)
        for v in T.vertices[u.num].adj:
            if v.cor == "branco":
                v.cor = "cinza"
                v.d = u.d + 1
                v.pai = u
                Q.append(v)
        u.cor = "preto"

    return u


def Diameter(T) -> int:
    s: Vertice = T.vertices[0]
    a: Vertice = LongestPathBFS(T, s)
    b: Vertice = LongestPathBFS(T, a)
    return b.d


def addEdgeFromFile(G: Grafo, line):
    spt = line.split()
    a: int = int(spt[0])
    b: int = int(spt[1])
    G.addAresta(a, b)
    return G


def createGraph(path):
    try:
        f = open(path, 'r')
    except FileNotFoundError:
        print("Arquivo inacessível...")
        return None
    numberOfVertices = int(f.readline())
    diameter = int(f.readline())

    G: Grafo = Grafo(numberOfVertices)

    line = f.readline()
    while line != '':
        addEdgeFromFile(G, line)
        line = f.readline()
    f.close()

    G.diameterAssertion = diameter
    return G


def main():
    inicio = timeit.default_timer()

    T = createGraph("./tests-files/" + fileTreeName + ".txt")
    d = Diameter(T)
    assert d == T.diameterAssertion

    fim = timeit.default_timer()
    print('duracao: %f' % (fim - inicio))


if __name__ == '__main__':
    main()
