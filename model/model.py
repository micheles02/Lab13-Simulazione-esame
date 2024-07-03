import networkx as nx
from geopy.distance import distance

from database.DAO import DAO


class Model:
    def __init__(self):
        self.anno = DAO.getYear()
        self.shape = DAO.getShape()
        self.graph = nx.Graph()
        self.idMap ={}
        self.solBest = 0
        self.path = [] #contiene i nodi da cui mi ricavo la distanza
        self.path_edge = [] #contiene gli archi e quindi i pesi

    def buildGraph(self, anno, shape):
        nodi =DAO.getNodes()
        for n in nodi:
            self.idMap[n.id] = n
            self.graph.add_node(n)
        peso = DAO.getPeso(anno, shape)
        for e in peso:
            self.graph.add_edge(self.idMap[e[0]], self.idMap[e[1]], weight = e[2])

    def sumPeso(self, year, shape):
        peso = DAO.getPeso(year, shape)
        result = []
        for n in self.graph.nodes:
            somma = 0
            for a in self.graph.edges(n, data=True):
                somma += a[2]["weight"]
            result.append((n.id, somma))
        return result

    def computePath(self):
        self.path = []
        self.path_edge = []

        for n in self.graph.nodes:
            partial = []
            partial.append(n)
            self.ricorsione(partial, []) #lista vuota perchè non ho una distanza in quanto ho solo un nodo

    def ricorsione(self, partial, partial_edge):
        n_last = partial[-1]

        neighbors = self.getAdmissibleNeighbs(n_last, partial_edge)

        # stop
        if len(neighbors) == 0:
            weight_path = self.computeWeightPath(partial_edge)
            if weight_path > self.solBest:
                self.solBest = weight_path + 0.0
                self.path = partial[:]
                self.path_edge = partial_edge[:]
            return
        else:
            for n in neighbors:
                partial_edge.append((n_last, n, self.graph.get_edge_data(n_last, n)['weight']))
                partial.append(n)

                self.ricorsione(partial, partial_edge)
                partial.pop()
                partial_edge.pop()
        #return
    def getAdmissibleNeighbs(self, n_last, partial_edges):
        all_neigh = self.graph.edges(n_last, data=True)
        result = []
        for e in all_neigh:
            if len(partial_edges) != 0:
                if e[2]["weight"] > partial_edges[-1][2]:
                    result.append(e[1])
            else:
                result.append(e[1])
        return result

    def computeWeightPath(self, mylist):
        weight = 0
        for e in mylist:
            weight += distance((e[0].Lat, e[0].Lng), (e[1].Lat, e[1].Lng)).km
        return weight

    def get_distance_weight(self, e):
        return distance((e[0].Lat, e[0].Lng), (e[1].Lat, e[1].Lng)).km


    def graph_details(self):
        return len(self.graph.nodes), len(self.graph.edges)

