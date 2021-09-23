import NetworkDefinitions as ND

def main():
    m = ND.NetworkDefinitions('karate.gml')

    N = m.getNodes()
    L = m.getLinks()
    K = m.getAverageDegree()
    LMax = m.getMaxEdges()
    Density = m.getDensity()

    print(f'N = {N}')
    print(f'L = {L}')
    print(f'<K> = {K}')
    print(f'LMax = {LMax}')
    print(f'Density = {Density:.6}')
    print(f'Max degree = {m.getMaxDegree()}')
    print(f'Min degree = {m.getMinimumDegree()}')

    m.networkToPdf()    
    m.getDegreeDistrib()

if __name__ == "__main__":
    main()