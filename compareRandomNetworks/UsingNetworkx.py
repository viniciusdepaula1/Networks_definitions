import numpy as np
import networkx as nx
import igraph as ig

from scipy.io import mmread

class UsingNetworkx:
    def __init__(self, networkName) -> None:

        # To summarize the following one-liner from SageMath, the solution involved reading the
        # file into a Scipy sparse matrix using mmread, then converting to a dense matrix, then
        # converting the matrix type to numpy, then using networkX to create the graph object.
        self.g = nx.Graph(
            np.matrix(mmread(networkName).todense()))

    def getNodes(self):
        return len(list(self.g.nodes))

    def getEdges(self):
        return len(list(self.g.edges))

    def average_degree(self):
        #node, degree = zip(*self.g.degree())
        degree = (x[1] for x in self.g.degree())
        return sum(degree)/self.getNodes()

    def getDegreeList(self):
        degree = (x[1] for x in self.g.degree())
        return list(degree)

    def get_average_connectivity(self):
        return nx.average_node_connectivity(self.g)

    def drawNetwork(self):
        self.toGml();
        graphNetwork = ig.Graph.Read_GML('generatedNetwork.gml')
        ig.plot(graphNetwork)

    def toGml(self):
        nx.write_gml(self.g, "generatedNetwork.gml")

    def returnGraph(self):
        return self.g