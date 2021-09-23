import numpy as np
import UsingNetworkx as un
from igraph import Graph
import matplotlib.pyplot as plt
import pandas as pd

def getDegreeDistrib(degreeList):
    maxk = np.max(degreeList)
    kvalues = np.arange(0, maxk+1)
    pk = np.zeros(maxk+1)

    for k in degreeList:
        pk[k] = pk[k] + 1

    pk = pk/sum(pk)

    return kvalues, pk


def plotDD(networkName, kvalues, pk):
    plt.figure()
    plt.loglog(kvalues, pk, 'bo')
    plt.xlabel("k", fontsize=20)
    plt.ylabel("P(k)", fontsize=20)
    plt.title(f"Degree distribution - {networkName}")
    plt.grid(True)
    plt.show()

def average_links(n, p):
    l = p * (n * (n-1))/2
    return l


def averageDegree(n, p):
    k = p * (n-1)
    if(k > 1):
        return (k, "supercritical")
    elif(k < 1):
        return (k, "subcritical")
    elif(k == 1):
        return (k, "critical point")
    elif(k > np.log(n) or p > (np.log(n)/n)):
        return (k, "connected regime")


def compareRandomNetwork(n, l):
    # find p from a defined network
    # average number of links formula
    p = (2 * l)/(n * (n-1))
    #p = '{0:.2g}'.format(calc)

    count = 0
    ksum = 0
    lsum = 0
    er = None

    while(count < 1000):
        er = Graph.Erdos_Renyi(n, p=p)
        ksum += int(sum(er.vs.degree())/er.vcount())
        lsum += er.ecount()
        count += 1

    # expected results
    l_expected = average_links(n, p)
    k_expected = averageDegree(n, p)[0]

    print("expected average degree: ", k_expected)
    print("expected average links: ", l_expected)

    print("found average degree: ", ksum/count)
    print("found average links: ", lsum/count)

    kv, pk = getDegreeDistrib(er.vs.degree())  #last roll
    plotDD("er_network", kv, pk)


def compareRealNetwork():
    g = un.UsingNetworkx('inf-USAir97.mtx')
    nodes = g.getNodes()
    edges = g.getEdges()
    degreeList = g.getDegreeList()
    
    print(f"Nodes: {nodes}") 
    print(f"Edges: {edges}")
    compareRandomNetwork(nodes, edges)

    kv, pk = getDegreeDistrib(degreeList)
    plotDD("original_network", kv, pk)
    return None


def main():
    #print(average_links(3000, 0.001))
    #print(averageDegree(3000, 0.001))
    #compareRandomNetwork(300, 900)
    compareRealNetwork()


if __name__ == "__main__":
    main()
