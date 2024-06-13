from database.DAO import DAO
import networkx as nx
from geopy import distance


class Model:
    def __init__(self):
        self._listSighting = []
        self._listShapes = []
        self._listStates = []

        self._grafo = nx.Graph()
        self._nodes = []
        self._edges = []
        self.solBest = 0

        self.path = []
        self.path_edge = []

        self.loadSighting()
        self.loadShapes()
        self.loadStates()

    def loadSighting(self):
        self._listSighting = DAO.getAllSighting()

    def loadShapes(self):
        self._listShapes = DAO.getAllShapes()

    def loadStates(self):
        self._listStates = DAO.getAllStates()

    @property
    def listSighting(self):
        return self._listSighting

    @property
    def listShapes(self):
        return self._listShapes

    @property
    def listStates(self):
        return self._listStates

    def buildGraph(self, s, a):
        self._grafo.clear()
        print(a, s)

        for p in self._listStates:
            self._nodes.append(p)

        self._grafo.add_nodes_from(self._nodes)
        self.idMap = {}
        for n in self._nodes:
            self.idMap[n.id] = n

        tmp_edges = DAO.getAllWeightedNeigh(a, s)

        for e in tmp_edges:
            self._edges.append((self.idMap[e[0]], self.idMap[e[1]], e[2]))

        self._grafo.add_weighted_edges_from(self._edges)

    def get_sum_weight_per_node(self):
        pp = []
        for n in self._grafo.nodes():
            sum_w = 0
            for e in self._grafo.edges(n, data=True):
                sum_w += e[2]['weight']
            pp.append((n.id, sum_w))
        return pp

    def computePath(self):
        self.path = []
        self.path_edge = []

        for n in self.get_nodes():
            partial = []
            partial.append(n)
            self.ricorsione(partial, [])

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

        for n in neighbors:
            partial_edge.append((n_last, n, self._grafo.get_edge_data(n_last, n)['weight']))
            partial.append(n)

            self.ricorsione(partial, partial_edge)
            partial.pop()
            partial_edge.pop()


    def getAdmissibleNeighbs(self, n_last, partial_edges):
        all_neigh = self._grafo.edges(n_last, data=True)
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
            weight += distance.geodesic((e[0].lat, e[0].lng), (e[1].lat, e[1].lng)).km
        return weight

    def get_distance_weight(self, e):
        return distance.geodesic((e[0].lat, e[0].lng), (e[1].lat, e[1].lng)).km

    def get_nodes(self):
        return self._grafo.nodes()

    def get_edges(self):
        return list(self._grafo.edges(data=True))

    def get_num_of_nodes(self):
        return self._grafo.number_of_nodes()

    def get_num_of_edges(self):
        return self._grafo.number_of_edges()
