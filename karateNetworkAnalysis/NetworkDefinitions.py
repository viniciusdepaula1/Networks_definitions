from igraph.drawing import plot
import numpy as np
import igraph as ig
import matplotlib.pyplot as plt
import pandas as pd

class NetworkDefinitions:
    graphNetwork = None
    N = None
    L = None

    def __init__(self, networkFile):
        self.graphNetwork = ig.Graph.Read_GML(networkFile)
        self.N = self.graphNetwork.vcount()
        self.L = self.graphNetwork.ecount()

    def getNodes(self):
        return self.N

    def getLinks(self):
        return self.L

    #<k> average degree
    def getAverageDegree(self):
        return int(sum(self.graphNetwork.vs.degree())/self.N)

    #L_{max} -- max number of edges in this network
    def getMaxEdges(self):
        x = self.N
        return (x*(x-1))/2

    #D density
    def getDensity(self):
        x = self.N
        y = self.L
        return (2 * y)/(x * (x - 1))

    def getMaxDegree(self):
        return self.graphNetwork.vs.maxdegree()

    def getMinimumDegree(self):
        return min(self.graphNetwork.vs.degree())

    #plot de p_k -- degree distrib -- matplotlib
    def getDegreeDistrib(self):
        df = pd.DataFrame(data=self.graphNetwork.vs.degree(), columns=['degree'])

        #dd = self.graphNetwork.degree_distribution()
        #print(dd)

        plt.hist(df, density=1, bins=20)
        plt.ylabel('Prob')
        plt.xlabel('Degree')
        plt.show()

    def networkToPdf(self):
        visual_style = {}
        visual_style["vertex_size"] = [i for i in self.graphNetwork.vs.degree()]
        visual_style["vertex_color"] = ['gray' if i < 15 else 'blue' for i in self.graphNetwork.vs.degree()]
        visual_style["bbox"] = (400, 400)
        visual_style["margin"] = 20
        visual_style["vertex_shape"] = 'circle'

        ig.plot(self.graphNetwork, "karate_network.pdf", **visual_style)