import numpy as np
import igraph as ig
import ts2vg as vg

class VG:
    def __init__(self) -> None:
        #csv_file = np.genfromtxt(tsFile, delimiter="\t");
        #series = csv_file[0:len(csv_file), 1];

        #visual_style = {}
        #visual_style["vertex_size"] = [i for i in nx_g.vs.degree()]
        #visual_style["vertex_color"] = ['gray' if i < 15 else 'blue' for i in nx_g.vs.degree()]
        #visual_style["bbox"] = (400, 400)
        #visual_style["margin"] = 20
        #visual_style["vertex_shape"] = 'circle'

        #ig.plot(nx_g, f"VG_Graph{tsFile}.pdf", **visual_style)
        pass

    def gen_network(self, serie):
        new_g = vg.NaturalVG()
        new_g.build(serie)
        igraph_network = new_g.as_igraph()

        return igraph_network
