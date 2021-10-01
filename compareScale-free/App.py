import os, sys
import matplotlib.pyplot as plt
from networkx import algorithms
from networkx import erdos_renyi_graph, expected_degree_graph
import numpy as np
from numpy.ma.core import default_fill_value

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from compareRandomNetworks import UsingNetworkx

def calcMetrics(graph):
    spl = dict(algorithms.all_pairs_shortest_path_length(graph))
    
    try:
        aspl = algorithms.average_shortest_path_length(graph)
    except:
        aspl = 0

    #print(f"spl: {spl}")
    
    listPaths = list()

    for node in spl:
        listPaths.extend((list(spl[node].values())))

    #print(listPaths[110223])

    maxD = np.max(listPaths)
    dValues = np.arange(0, maxD+1)

    pd = np.zeros(maxD+1)
    for d in listPaths:
        pd[d] = pd[d] + 1

    pd = pd/sum(pd)

    #print(f'sum pd = {sum(pd)}')
    #print(pd)

    #for node in [0, 331]:
    #    print(f"1 - {node}: {spl[331][node]}")

    print(f"aspl: {aspl}")

    return dValues, pd

def generateG(nodes, edges):
    p = (2 * edges)/(nodes * (nodes-1))
    
    graph = erdos_renyi_graph(nodes, p)

    dValues, pd = calcMetrics(graph)

    return dValues, pd

def generateDPR(graph):
    degrees = [val for (node, val) in graph.degree()]

    g = expected_degree_graph(degrees)

    dValues, pd = calcMetrics(g)

    return dValues, pd

def main():
    g = UsingNetworkx.UsingNetworkx('inf-USAir97.mtx')
    nodes = g.getNodes()
    edges = g.getEdges()
    
    print(f"1-- Nodes: {nodes}") 
    print(f"1-- Edges: {edges}")

    graph1 = g.returnGraph()

    dValues1, pd1 = calcMetrics(graph1)
    dValues2, pd2 = generateG(nodes, edges)
    dValues3, pd3 = generateDPR(graph1)

    plt.figure()
    plt.plot(dValues1, pd1, label="Original Network")
    plt.plot(dValues2, pd2, label="Erdos_Renyi Network")
    plt.plot(dValues3, pd3, label="Degree preserving randomization")
    plt.xlabel("d", fontsize=20)
    plt.ylabel("P(d)", fontsize=20)
    plt.legend()
    plt.title(f"Distance Distribution - inf-USAir97")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
    