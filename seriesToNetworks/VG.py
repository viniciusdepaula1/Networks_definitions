from typing import Tuple
import numpy as np
from igraph import *
from visibility_graph import visibility_graph
from itertools import combinations
import networkx as nx

class VG:
    def __init__(self, tsFile: str) -> None:
        csv_file = np.genfromtxt(tsFile, delimiter="\t");
        series = csv_file[0:len(csv_file), 1];
        g = self.serieToVg(series);
        
        visual_style = {}
        visual_style["vertex_size"] = [i for i in g.vs.degree()]
        visual_style["vertex_color"] = ['gray' if i < 15 else 'blue' for i in g.vs.degree()]
        visual_style["bbox"] = (400, 400)
        visual_style["margin"] = 20
        visual_style["vertex_shape"] = 'circle'

        plot(g, "VG_Graph.pdf", **visual_style)


    def serieToVg(self, series):
        g = nx.Graph()

        # convert list of magnitudes into list of tuples that hold the index
        tseries = []
        n = 0
        for magnitude in series:
            tseries.append( (n, magnitude ) )
            n += 1

        # contiguous time points always have visibility
        for n in range(0,len(tseries)-1):
            (ta, ya) = tseries[n]
            (tb, yb) = tseries[n+1]
            g.add_node(ta, mag=ya)
            g.add_node(tb, mag=yb)
            g.add_edge(ta, tb)

        for a,b in combinations(tseries, 2):
            # two points, maybe connect
            (ta, ya) = a
            (tb, yb) = b

            connect = True
            
            # let's see all other points in the series
            for tc, yc in tseries[ta:tb]:
                # other points, not a or b
                if tc != ta and tc != tb:
                    # does c obstruct?
                    if yc > yb + (ya - yb) * ( (tb - tc) / (tb - ta) ):
                        connect = False
                        
            if connect:
                g.add_edge(ta, tb)


        return Graph.from_networkx(g)