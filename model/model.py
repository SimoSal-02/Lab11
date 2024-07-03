import copy

import networkx as nx
from matplotlib import pyplot as plt

from database.DAO import DAO



class Model:
    def __init__(self):
        self._allProduct = None
        self._idMap={}
        self._grafo=nx.Graph()
        self._bestSol=[]

    def getColor(self):
        return DAO.getAllColor()

    def creaGrafo(self,color,anno):
        self._grafo.clear()
        self._allProduct=DAO.getAllProduct(color)
        self._grafo.add_nodes_from(self._allProduct)
        for product in self._allProduct:
            self._idMap[product.Product_number]=product

        for p1 in self._allProduct:
            for p2 in self._allProduct:
                if p1!=p2 and p1.Product_number<p2.Product_number:
                    archi=DAO.getArchi(p1.Product_number,p2.Product_number,anno,self._idMap)
                    for a in archi:
                        self._grafo.add_edge(a[0],a[1],weight=a[2])
        sorted_edges = sorted(self._grafo.edges(data=True),key=lambda x: x[2]['weight'],reverse=True)
        #self.printGraph()
        return self._grafo.number_of_nodes(),sorted_edges

    def getNodes(self):
        return sorted(self._grafo.nodes())

    def bestPath(self,v0):
        print(self._idMap)
        parziale=[]
        archiVicini=[(u,v,self._grafo.get_edge_data(u, v)['weight']) for u,v in self._grafo.edges(self._idMap[int(v0)])]
        print(archiVicini)
        for a in archiVicini:
            parziale.append(a)
            pesoUltimo=a[2]
            print(pesoUltimo)
            self.ricorsione(parziale,pesoUltimo)
            parziale.pop()

        return len(self._bestSol)

    def ricorsione(self,parziale,pesoUltimo):
        v0=parziale[-1]
        archiVicini = [(u,v,self._grafo.get_edge_data(u, v)['weight']) for u,v in self._grafo.edges(v0[1])]
        for a in archiVicini:
            if self.isAmmissibile(parziale, a, pesoUltimo):
                parziale.append(a)
                self.ricorsione(parziale,a[2])
                if len(parziale) > len(self._bestSol):
                    self._bestSol= copy.deepcopy(parziale)
                parziale.pop()

    def isAmmissibile(self,parziale,a,pesoUltimo):
        if (a not in parziale) and ((a[1],a[0],a[2]) not in parziale) and a[2] >= pesoUltimo:
            return True
        else:
            return False


    def printGraph(self):
        plt.figure(figsize=(50, 50))

        pos = nx.spring_layout(self._grafo)  # pos = nx.nx_agraph.graphviz_layout(G)
        nx.draw_networkx(self._grafo, pos)
        labels = nx.get_edge_attributes(self._grafo, 'weight')
        nx.draw_networkx_edge_labels(self._grafo, pos, edge_labels=labels)

        plt.savefig("plot")
        plt.show()



