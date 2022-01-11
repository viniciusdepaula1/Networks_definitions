import numpy as np
import igraph as ig

class DCTIF:

    def __init__(self) -> None:
       pass

    def gen_network(self, serie):
        #csv_file = np.genfromtxt(serie, delimiter="\t")
        
        N = 1000
        count = 0

        g = ig.Graph()
        g.add_vertices(N)
        for i in range(N):
            g.vs[i]["label"] = i+1

        x = serie[count]
        index = int(self.integralFunction(x, N))

        for i in range(len(serie)):
            x = serie[count+i]
            print(x)
            print(index)

            indexAnterior = index

            index = int(self.integralFunction(x, N))

            #print('index= ', index);
            self.addEdge(g, indexAnterior-1, index-1)

        graphAux = ig.Graph()
        numVertices = 0
        labels = []

        for i in g.vs:
            if i.degree() > 0:
                numVertices = numVertices + 1
                labels.append(i["label"])

        #print('labels= ', labels);
        #print('numVertices= ', numVertices);
        #print('numArestas= ', len(g.es));

        graphAux.add_vertices(numVertices)
        for i in range(numVertices):
            graphAux.vs[i]["label"] = labels[i]

        for i in range(len(g.es)):
            src = g.vs[g.es[i].source]["label"]
            dst = g.vs[g.es[i].target]["label"]

            print('src= ', src);
            print('dst= ', dst);

            if(src != dst):
                src_ = 0
                dst_ = 0
                for j in graphAux.vs:
                    if j["label"] == src:
                        src_ = j.index
                    if j["label"] == dst:
                        dst_ = j.index
                graphAux.add_edge(src_, dst_)

        #ig.plot(graphAux)
        
        return graphAux
        

    def integralFunction(self, num: int, N: int) -> int:
        result = int()

        if (num*N) == 0:
            result = int(1)
        elif (round(num*N) - num*N) >= 0.0:
            result = int(round(num*N))
        else:
            result = int(round(num*N) + 1.0)

        return result

    def addEdge(self, g, v1, v2):
        if g.get_eid(v1, v2, directed=False, error=False) == -1:
            g.add_edge(v1, v2)
