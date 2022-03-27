from tkinter import font
from numpy import arange, ndarray
from src.ClassicMethods import *
from src.DCTIF import *
from src.DCSD import *
from src.VG import *
from scipy import stats

from src.portrait_divergence.portrait_divergence import portrait_divergence
import src.TemporalSerie as TS
import pandas as pd
import csv
import plotly.express as px
from scipy import stats
import netlsd
import sklearn.feature_selection._mutual_info as mmmi
import os
import plotly.graph_objects as go

def plotResults():
    allData = pd.read_csv('./networks_results/gcd11_results/HVG_GCD11.csv');
    fig = px.line(allData, x = 'Intensity', y = ['Average Distance', 'Min Distance', 'Max Distance'], title = 'VG NETWORKS COMPARISON WITH GCD-11');
    fig.show()

def plotBoxPlot():
    vg_data = pd.read_csv('./BoxPlot_VG_NETLSD_Results.csv');
    dcsd_data = pd.read_csv('./BoxPlot_DCSD_NetLSD_Results.csv');
    dctif_data = pd.read_csv('./BoxPlot_DCTIF_NetLSD_Results.csv');

    fig = go.Figure()

    #VG_PLOTS
    fig.add_trace(go.Box(
        y = vg_data['0.0'],
        name='0.0',
        marker_color = 'green'
    ))

    fig.add_trace(go.Box(
        y = vg_data['0.05'],
        name='0.05',
        marker_color = 'green'
    ))

    fig.add_trace(go.Box(
        y = vg_data['0.25'],    
        name='0.25',
        marker_color = 'green'
    ))

    fig.add_trace(go.Box(
        y = vg_data['0.4'],    
        name='0.4',
        marker_color = 'green'
    ))

    #DCSD_PLOTS
    fig.add_trace(go.Box(
        y = dcsd_data['0.0'],
        name='0.0',
        marker_color = 'blue'
    ))

    fig.add_trace(go.Box(
        y = dcsd_data['0.05'],
        name='0.05',
        marker_color = 'blue'
    ))

    fig.add_trace(go.Box(
        y = dcsd_data['0.25'],
        name='0.25',
        marker_color = 'blue'
    ))

    fig.add_trace(go.Box(
        y = dcsd_data['0.4'],
        name='0.4',
        marker_color = 'blue'
    ))

    #DCTIF_PLOTS
    fig.add_trace(go.Box(
        y = dctif_data['0.0'],
        name='0.0',
        marker_color = 'red'
    ))

    fig.add_trace(go.Box(
        y = dctif_data['0.05'],
        name='0.05',
        marker_color = 'red'
    ))

    fig.add_trace(go.Box(
        y = dctif_data['0.25'],
        name='0.25',
        marker_color = 'red'
    ))

    fig.add_trace(go.Box(
        y = dctif_data['0.4'],
        name='0.4',
        marker_color = 'red'
    ))

    fig.update_layout(
        font=dict(
            family="Courier New, monospace",
            size=40,
            color="Black"
        ),
        boxmode='group',
        yaxis_title="Similaridade",
    )
        

    fig.show()

    #print(allData['0.0'])
    #fig = px.box(allData['0.05'], y='0.05')
    #fig.show()

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
    toLeda(network2, './src/GCD-11/count/network2.gw')
    os.system("(cd ./src/GCD-11/count && python count.py network2.gw)")
    os.system("(cd ./src/GCD-11 && python3 networkComparison.py ./count 'gcd11' 1)")
    vg_results.append(readResults());

def hvgGCD11(serie2, hvg_results, iValue): 
    s1X, s1Y = serie2.addNoise(iValue)
    graph2 = VG()
    network2 = graph2.gen_horizontal_network(s1Y)
    toLeda(network2, './src/GCD-11/count/network2.gw')
    os.system("(cd ./src/GCD-11/count && python count.py network2.gw)")
    os.system("(cd ./src/GCD-11 && python3 networkComparison.py ./count 'gcd11' 1)")
    hvg_results.append(readResults());

def dcsdGCD11(serie2, dcsd_results, iValue):
    s1X, s1Y = serie2.addNoise(iValue)
    graph2 = DCSD()
    network2 = graph2.gen_network(s1Y)
    toLeda(network2, './src/GCD-11/count/network2.gw')
    os.system("(cd ./src/GCD-11/count && python count.py network2.gw)")
    os.system("(cd ./src/GCD-11 && python3 networkComparison.py ./count 'gcd11' 1)")
    dcsd_results.append(readResults())

def dctifGCD11(serie2, dctif_results, iValue):
    s1X, s1Y = serie2.addNoise(iValue)
    graph2 = DCTIF()
    network2 = graph2.gen_network(s1Y)
    toLeda(network2, './src/GCD-11/count/network2.gw')
    os.system("(cd ./src/GCD-11/count && python count.py network2.gw)")
    os.system("(cd ./src/GCD-11 && python3 networkComparison.py ./count 'gcd11' 1)")
    dctif_results.append(readResults())
    
def readResults():
    file = open('./src/GCD-11/count/gcd11.txt')
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

def hvgNetLSD(desc1, serie2, vg_results, iValue):
    s1X, s1Y = serie2.addNoise(iValue)
    graph2 = VG()
    network2 = graph2.gen_horizontal_network(s1Y)
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

def hvgPortrait(network1, serie2, vg_results, iValue):
    s1X, s1Y = serie2.addNoise(iValue)
    graph2 = VG()
    network2 = graph2.gen_horizontal_network(s1Y)
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

    results0 = []
    results005 = []
    results025 = []
    results04 = []

    #iValues = np.linspace(0.001, 0.4, 400);  #(0.001, 0.4, 400) (0.01, 0.4, 40) (10, 4000, 400)
    iValues = [0.0, 0.05, 0.25, 0.4];

    serie1.genSineSerie(0, 30, 0.1, 5)
    serie2.genSineSerie(0, 30, 0.1, 5)

    graph1 = DCTIF();
    network1 = graph1.gen_network(serie1.serieY);
    desc = netlsd.heat(network1)

    for i in range(len(iValues)):
        for j in range(100):
            func(desc, serie2, results, iValues[i]);

        if(i == 0):
            results0 = results
        if(i == 1):
            results005 = results
        if(i == 2): 
            results025 = results
        if(i == 3):
            results04 = results

        #averageResults.append(np.mean(results));   
        #maxResults.append(np.max(results));
        #minResults.append(np.min(results));

        #print(averageResults)
        #print(maxResults)
        #print(minResults)

        results = []
    
    f = open(fileName, "w+");
    writer = csv.writer(f);
    #header = ['Intensity', 'Average Distance', 'Min Distance', 'Max Distance'];
    header = ['0.0', '0.05', '0.25', '0.4'];
    writer.writerow(header)

    #for i in range(len(iValues)):
    #    data = [iValues[i], averageResults[i], minResults[i], maxResults[i]];
    #    writer.writerow(data);

    for i in range(len(results0)):
        data = [results0[i], results005[i], results025[i], results04[i]];
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

#0.0, 0.05, 0.25, 0.4
def genSeriesImage():
    serie1 = TS.TemporalSerie()
    serie2 = TS.TemporalSerie()
    serie3 = TS.TemporalSerie()
    serie4 = TS.TemporalSerie()

    serie1.genSineSerie(0, 30, 0.5, 5)
    serie2.genSineSerie(0, 30, 0.5, 5)
    serie3.genSineSerie(0, 30, 0.5, 5)
    serie4.genSineSerie(0, 30, 0.5, 5)

    s2X, s2Y = serie2.addNoise(0.05)
    s3X, S3Y = serie3.addNoise(0.25)
    s4X, S4Y = serie4.addNoise(0.4)

    serie1.plotMultipleSeries(s2Y, S3Y, S4Y);

if __name__ == "__main__":
    #serie_similaridade_x_intensidade("dtwResults.csv", calcI)
    #serie_similaridade_x_intensidade("pearsonResults.csv", calcPearson)
    #serie_similaridade_x_intensidade("miResults.csv", calcMi)
    
    #mergeResults()
    #plotResults()
    #genSeriesImage()
        
    #network_similaridade_x_intensidade("BoxPlot_VG_NETLSD_Results.csv", vgNetLSD)
    #network_similaridade_x_intensidade("BoxPlot_DCSD_NetLSD_Results.csv", dcsdNetLSD)
    #network_similaridade_x_intensidade("BoxPlot_DCTIF_NetLSD_Results.csv", dctifNetLSD)
    
    #network_similaridade_x_intensidade("DCTIF_NETLSD1.csv", dctifNetLSD)
    #network_similaridade_x_intensidade("HVG_PORTRAIT.csv", hvgPortrait)

    plotBoxPlot()