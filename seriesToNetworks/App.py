from numpy import arange, ndarray
from ClassicMethods import *
from DCTIF import *
from DCSD import *
from VG import *
from scipy import stats

from portrait_divergence.portrait_divergence import portrait_divergence
import TemporalSerie as TS
import pandas as pd
import csv
import plotly.express as px
from scipy import stats
import netlsd
import sklearn.feature_selection._mutual_info as mmmi
import os

def plotResults():
    allData = pd.read_csv('DCTIF_PORTRAIT.csv');
    fig = px.line(allData, x = 'Intensity', y = ['Average Distance', 'Min Distance', 'Max Distance'], title = 'VG NETWORKS COMPARISON WITH GCD-11');
    fig.show()


# Classic functions -- distance
def calcDTW(serie1, serie2, dtwResults, iValue):
    s1X, s1Y = serie1.addNoise(iValue)
    dtwAlignment = ClassicMethods.calcDTW(s1Y, serie2.serieY, False)
    dtwResults.append(dtwAlignment)

def calcPearson(serie1, serie2, pearsonResults, iValue):
    s1X, s1Y = serie1.addNoise(iValue)
    r, pValue = stats.pearsonr(s1Y, serie2.serieY)
    pearsonResults.append(r);

def calcMi(serie1, serie2, miResults, iValue):
    s1X, s1Y = serie1.addNoise(iValue)
    mi2 = mmmi._compute_mi_cc(s1Y, serie2.serieY, 4)   #k=4 || k=6
    miResults.append(mi2);


# Hamming distance function
def calcHd(adj_matrix, serie2, hdResults, iValue):
    s1X, s1Y = serie2.addNoise(iValue)
    
    graph2 = DCTIF();
    net2 = graph2.gen_network(s1Y)
    adj2 = net2.get_adjacency();

    len1 = adj_matrix.shape[0] * adj_matrix.shape[1]
    len2 = adj2.shape[0] * adj2.shape[1]

    minLen = None

    if len1 > len2:
        minLen = adj2
    else:
        minLen = adj_matrix

    max_adj = max([len1, len2])
    min_adj = min([len1, len2])

    diff = max_adj - min_adj

    countDiff = 0

    for i in range(minLen.shape[0]):
        for j in range(minLen.shape[1]):
            if(adj_matrix[i][j] != adj2[i][j]):
                countDiff += 1
    
    countDiff += diff

    hdResults.append(countDiff)   
    

#GCD-11 functions
def vgGCD11(serie2, vg_results, iValue): 
    s1X, s1Y = serie2.addNoise(iValue)
    graph2 = VG()
    network2 = graph2.gen_network(s1Y)
    toLeda(network2, './GCD-11/count/network2.gw')
    os.system("(cd ./GCD-11/count && python count.py network2.gw)")
    os.system("(cd ./GCD-11 && python3 networkComparison.py ./count 'gcd11' 1)")
    vg_results.append(readResults());

def dcsdGCD11(serie2, dcsd_results, iValue):
    s1X, s1Y = serie2.addNoise(iValue)
    graph2 = DCSD()
    network2 = graph2.gen_network(s1Y)
    toLeda(network2, './GCD-11/count/network2.gw')
    os.system("(cd ./GCD-11/count && python count.py network2.gw)")
    os.system("(cd ./GCD-11 && python3 networkComparison.py ./count 'gcd11' 1)")
    dcsd_results.append(readResults())

def dctifGCD11(serie2, dctif_results, iValue):
    s1X, s1Y = serie2.addNoise(iValue)
    graph2 = DCTIF()
    network2 = graph2.gen_network(s1Y)
    toLeda(network2, './GCD-11/count/network2.gw')
    os.system("(cd ./GCD-11/count && python count.py network2.gw)")
    os.system("(cd ./GCD-11 && python3 networkComparison.py ./count 'gcd11' 1)")
    dctif_results.append(readResults())
    
def readResults():
    file = open('./GCD-11/count/gcd11.txt')
    file.readline()
    results = file.readline().split('\t')
    final = results[2].rstrip()
    return float(final)

def toLeda(network1, file_name):
    network1.write_leda(file_name, names=None, weights=None)


#NetLSD functions
def vgNetLSD(desc1, serie2, vg_results, iValue):
    s1X, s1Y = serie2.addNoise(iValue)
    graph2 = VG()
    network2 = graph2.gen_network(s1Y)
    desc2 = netlsd.heat(network2);
    distance = netlsd.compare(desc1, desc2);
    vg_results.append(distance)

def dcsdNetLSD(desc1, serie2, dcsd_results, iValue):
    s1X, s1Y = serie2.addNoise(iValue)
    graph2 = DCSD()
    network2 = graph2.gen_network(s1Y)
    desc2 = netlsd.heat(network2);
    distance = netlsd.compare(desc1, desc2)
    dcsd_results.append(distance)

def dctifNetLSD(desc1, serie2, dctif_results, iValue):
    s1X, s1Y = serie2.addNoise(iValue)
    graph2 = DCTIF()
    network2 = graph2.gen_network(s1Y)
    desc2 = netlsd.heat(network2);
    distance = netlsd.compare(desc1, desc2)
    dctif_results.append(distance)


#Portrait_divergence functions  (only networkx)
def vgPortrait(network1, serie2, vg_results, iValue):
    s1X, s1Y = serie2.addNoise(iValue)
    graph2 = VG()
    network2 = graph2.gen_network(s1Y)
    vg_results.append(portrait_divergence(network1, network2))

def dcsdPortrait(network1, serie2, dcsd_results, iValue):
    s1X, s1Y = serie2.addNoise(iValue)
    graph2 = DCSD()
    network2 = graph2.gen_network(s1Y)
    dcsd_results.append(portrait_divergence(network1, network2))

def dctifPortrait(network1, serie2, dctif_results, iValue):
    s1X, s1Y = serie2.addNoise(iValue)
    graph2 = DCTIF()
    network2 = graph2.gen_network(s1Y)
    dctif_results.append(portrait_divergence(network1, network2))


#Network distance calc
def network_similaridade_x_intensidade(fileName, func): 
    serie1 = TS.TemporalSerie()
    serie2 = TS.TemporalSerie()

    results = []

    maxResults = []
    minResults = []
    averageResults = []

    iValues = np.linspace(0.001, 0.4, 400);  #(0.001, 0.4, 400) (0.01, 0.4, 40) (10, 4000, 400)

    serie1.genSineSerie(0, 30, 0.1, 5)
    serie2.genSineSerie(0, 30, 0.1, 5)

    graph1 = DCTIF();
    network1 = graph1.gen_network(serie1.serieY);

    for i in range(len(iValues)):
        for j in range(100):
            func(network1, serie2, results, iValues[i]);

        averageResults.append(np.mean(results));   
        maxResults.append(np.max(results));
        minResults.append(np.min(results));

        print(averageResults)
        print(maxResults)
        print(minResults)

        results = []
    
    f = open(fileName, "w+");
    writer = csv.writer(f);
    header = ['Intensity', 'Average Distance', 'Min Distance', 'Max Distance'];
    writer.writerow(header)

    for i in range(len(iValues)):
        data = [iValues[i], averageResults[i], minResults[i], maxResults[i]];
        writer.writerow(data);


#Series distance calc
def serie_similaridade_x_intensidade(fileName, func): #pearson, mi, dtw
    serie1 = TS.TemporalSerie()
    serie2 = TS.TemporalSerie()

    results = []

    maxResults = []
    minResults = []
    averageResults = []

    iValues = np.linspace(0.001, 0.4, 400);  #(0.001, 0.4, 400) (0.01, 0.4, 40) (10, 4000, 400)

    serie1.genSineSerie(0, 30, 0.1, 5)
    serie2.genSineSerie(0, 30, 0.1, 5)

    for i in range(len(iValues)):
        for j in range(1000):
            func(serie1, serie2, results, iValues[i]);

        averageResults.append(np.mean(results));   
        maxResults.append(np.max(results));
        minResults.append(np.min(results));

        results = []

    f = open(fileName, "w+");
    writer = csv.writer(f);
    header = ['Intensity', 'Average Distance', 'Min Distance', 'Max Distance'];
    writer.writerow(header)

    for i in range(len(iValues)):
        data = [iValues[i], averageResults[i], minResults[i], maxResults[i]];
        writer.writerow(data);




if __name__ == "__main__":
    #serie_similaridade_x_intensidade("dtwResults.csv", calcI)
    #serie_similaridade_x_intensidade("pearsonResults.csv", calcPearson)
    #serie_similaridade_x_intensidade("miResults.csv", calcMi);
    
    #mergeResults()
    #plotResults();
    
    #network_similaridade_x_intensidade("HD_VG.csv", calcVG)
    
    #network_similaridade_x_intensidade("GCD11_Result.csv", vgGCD11)
    #network_similaridade_x_intensidade("DCSD_GCD11.csv", dcsdGCD11)
    #network_similaridade_x_intensidade("DCTIF_NETLSD1.csv", dctifNetLSD)

    network_similaridade_x_intensidade("DCTIF_PORTRAIT.csv", dctifPortrait)
