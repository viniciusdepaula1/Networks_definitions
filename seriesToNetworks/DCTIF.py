from typing import Set
import numpy as np
import igraph as ig

class DCTIF:

    def __init__(self, tsFile: str) -> None:
        csv_file = np.genfromtxt(tsFile, delimiter="\t")
        print(len(csv_file))
        N = 10000
        count = 0

        g = ig.Graph()
        g.add_vertices(N)
        for i in range(N):
            g.vs[i]["label"] = i+1

        x = csv_file[count, 1]
        print(x);
        index = int(self.integralFunction(x, N))

        for i in range(len(csv_file)):
            x = csv_file[count+i, 1]
            print(x)
            print(index)

            indexAnterior = index

            index = int(self.integralFunction(x, N))

            print('index= ', index);
            self.addEdge(g, indexAnterior-1, index-1)

        graphAux = ig.Graph()
        numVertices = 0
        labels = []

        for i in g.vs:
            if i.degree() > 0:
                numVertices = numVertices + 1
                labels.append(i["label"])

        print('labels= ', labels);
        print('numVertices= ', numVertices);
        print('numArestas= ', len(g.es));

        graphAux.add_vertices(numVertices)
        for i in range(numVertices):
            graphAux.vs[i]["label"] = labels[i]

        for i in range(len(g.es)):
            src = g.vs[g.es[i].source]["label"]
            dst = g.vs[g.es[i].target]["label"]

            print('src= ', src);
            print('dst= ', dst);

            src_ = 0
            dst_ = 0
            for j in graphAux.vs:
                if j["label"] == src:
                    src_ = j.index
                if j["label"] == dst:
                    dst_ = j.index
            graphAux.add_edge(src_, dst_)

        #return graphAux
        visual_style = {}
        visual_style["vertex_size"] = [i for i in graphAux.vs.degree()]
        visual_style["vertex_color"] = ['gray' if i < 15 else 'blue' for i in graphAux.vs.degree()]
        visual_style["bbox"] = (400, 400)
        visual_style["margin"] = 20
        visual_style["vertex_shape"] = 'circle'

        ig.plot(graphAux, f"DCTIF_Graph{tsFile}.pdf", **visual_style)
        pass

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
