from typing import Tuple
from igraph import datatypes
from igraph.drawing import graph
import numpy as np
import networkx as nx
from igraph import *


class DCSD:
    def __init__(self, tsFile) -> None:
        csv_file = np.genfromtxt(tsFile, delimiter="\t");
        meio = middlePoint(csv_file)
        base = 2
        nn = 10

        vet_x = csv_file[0:len(csv_file), 1]
        print(vet_x)

        vetor_binario = self.calcula_vetor_binario(vet_x, meio);
        vet_decimal = self.vetor_bi2decimal(vetor_binario, nn);
        g = self.to_networkx(vet_decimal,nn,base);
        #mat_adj_nova = self.calcula_matriz_adj_soh_dos_nohs_conectados(mat_adj);
        #grafoFinal = nx.from_numpy_matrix(mat_adj_nova)

        #return graphAux
        visual_style = {}
        visual_style = {}
        visual_style["vertex_size"] = [i for i in g.vs.degree()]
        visual_style["vertex_color"] = ['gray' if i < 15 else 'blue' for i in g.vs.degree()]
        visual_style["bbox"] = (400, 400)
        visual_style["margin"] = 20
        visual_style["vertex_shape"] = 'circle'

        plot(g, "DCSD_Graph.pdf", **visual_style)
        pass

    def calcula_vetor_binario(self, x, meio):
        #recebe um vetor x e transforma ele em um vetor binario. aqui x vai de -1 ate 1. 
        #se x >= 0 vou dar valor de 1 se x <0 vou dar valor zero
        #retorna vetor binario com 0 e 1 de tamanho len(x)
        

        vet_binario = np.zeros(len(x))
        
        for i in range(len(x)):
            if x[i] >=meio:
                vet_binario[i] = 1
            else:
                vet_binario[i] = 0
        
        return(vet_binario.astype(int))

    def vetor_bi2decimal(self, vet_bi, n):
        #recebe vetor binario e vai pegar numero de tamanho n pra transformar pra decimal. anda de um em um
        #n = tamanho da palavra
        #retorna vetor decimal 
        tam = len(vet_bi)
        
        vet_dec = np.zeros(0)

        
        for i in range(tam-n+1) :#precisa ir ate tam-n 
            
            v = vet_bi[i:i+n]
            string_v = ''
            for j in range(len(v)): #transforma o vetor v em string
                string_v = string_v + str(v[j])
                        
            vet_dec = np.append(vet_dec,int(string_v,2))
        return(vet_dec.astype(int));

    def to_networkx(self, vet_dec, n, base):
        #tenho no maximo N = 2^n vertices no grafo. n = tamanho da palavra escolhida na hora da conversao
        #vet_dec(i) se conecta com seu vizinho vet_dec(i+1)
        tam_mat = base**n
        count = 0
        g = Graph()
        g.add_vertices(tam_mat)
        for i in range(tam_mat):
            g.vs[i]["label"] = i+1

        valor = vet_dec[count]

        for i in range(1, len(vet_dec)):
            prox_valor = vet_dec[i]
            addEdge(g, valor, prox_valor)
            valor = prox_valor;


        graphAux = Graph()
        numVertices = 0
        labels = []

        for i in g.vs:
            if i.degree() > 0:
                numVertices = numVertices + 1;
                labels.append(i["label"])

        print('labels= ', labels)

        print('numVertices= ', numVertices)
    
        print('numArestas= ', len(g.es))
        graphAux.add_vertices(numVertices);

        for i in range(numVertices):
            graphAux.vs[i]["label"] = labels[i]
    
        for i in range(len(g.es)):
            src = g.vs[g.es[i].source]["label"]
            dst = g.vs[g.es[i].target]["label"]

            print('src= ', src)
            print('dst= ', dst)

            src_ = 0
            dst_ = 0

            for j in graphAux.vs:
                if j["label"] == src:
                    src_ = j.index
                if j["label"] == dst:
                    dst_ = j.index

            graphAux.add_edge(src_, dst_);

        return graphAux

def middlePoint(csv_file) -> int:
    menor = 99999
    maior = -99999

    for i in range(len(csv_file)):
        if menor > csv_file[i, 1]:
            menor = csv_file[i, 1]
        if maior < csv_file[i, 1]:
            maior = csv_file[i, 1]

    return (maior + menor) / 2

def addEdge(g, v1, v2):
    if g.get_eid(v1, v2, directed=False, error=False) == -1:
        g.add_edge(v1, v2)