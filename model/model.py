import copy
import random
from math import sqrt
#from geopy.distance import geodesic

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.graph = nx.Graph()

    def buildGraph(self, loc):
        self.graph.clear()
        self.graph.add_nodes_from(loc)
        listaArchi = DAO.getEdges()
        for a in listaArchi:
            self.graph.add_edge(a[0], a[1], weight= a[2])

    def statistiche(self, localizzazione):
        vicini = self.graph.neighbors(localizzazione)
        result = {}
        for v in vicini:
            value = self.graph[localizzazione][v]["weight"]
            result[v] = value
        return result

    def calcolaCammino(self, inizio):
        self.solBest = []
        parziale = [inizio]
        self.lunghezzaMax = 0
        self.ricorsione(parziale, inizio)
        a = 0
        return self.solBest,self.lunghezzaMax


    def ricorsione(self, parziale, n):
        vicini = list(self.graph.neighbors(n))
        if not self.check(vicini, parziale, n):
            lunghezza = self.calcolaLunghezza(parziale)
            if lunghezza > self.lunghezzaMax:
                self.solBest = copy.deepcopy(parziale)
                self.lunghezzaMax = lunghezza
        for v in vicini:
            if self.vincoli(parziale, n, v):
                parziale.append(v)
                print(parziale)
                self.ricorsione(parziale, v)
                parziale.pop()
        if len(parziale) == 1:
            return



    def check(self, vicini, parziale, nodo):
        return any(self.vincoli(parziale, nodo, v) for v in vicini)

    def vincoli(self, parziale, nodo, vicino):
        for i in range(len(parziale)-1):
            if {nodo, vicino} == {parziale[i], parziale[i+1]}:
                return False
        return True

    def calcolaLunghezza(self, parziale):
        lunghezza = 0
        for i in range(len(parziale)-1):
            lunghezza += self.graph[parziale[i]][parziale[i+1]]["weight"]
        return lunghezza


    def graphDetails(self):
        return len(self.graph.nodes), len(self.graph.edges)