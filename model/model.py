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
        viciniAccettabili = self.cercaAccettabili(vicini, n, parziale)
        if len(viciniAccettabili) == 0:
            lunghezza = self.calcolaLunghezza(parziale)
            if lunghezza > self.lunghezzaMax:
                print(lunghezza, self.solBest)
                self.solBest = copy.deepcopy(parziale)
                self.lunghezzaMax = lunghezza
                return
        for v in viciniAccettabili:
            parziale.append(v)
            #print(parziale)
            self.ricorsione(parziale, v)
            parziale.pop()
        if len(parziale) == 1:
            return

    def cercaAccettabili(self, vicini, n, parziale):
        neigh = []
        for v in vicini:
            if v not in parziale:
                neigh.append(v)


        return neigh



    def calcolaLunghezza(self, parziale):
        lunghezza = 0
        for i in range(len(parziale)-1):
            lunghezza += self.graph[parziale[i]][parziale[i+1]]["weight"]
        return lunghezza


    def graphDetails(self):
        return len(self.graph.nodes), len(self.graph.edges)