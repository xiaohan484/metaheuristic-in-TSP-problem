from ImprovedAntColony import *
from ga import *
from antSystem import *
from antColony import *
import matplotlib.pyplot as plt



if __name__=='__main__':
    TSP_problem="xqf131"
    NC=109
    fileName=TSP_problem+".tsp"
    
    tsp=ImprovedAntColony()
    tsp.readfile(fileName)
    tsp.gothrough(NC)
    tsp.toExcel(TSP_problem+"ImprovedAntColony.xlsx")
    plt.close()

    tsp=GA()
    tsp.readfile(fileName)
    tsp.gothrough(NC)
    tsp.toExcel(TSP_problem+"GA.xlsx")
    plt.close()

    tsp=AntColony()
    tsp.readfile(fileName)
    tsp.gothrough(NC)
    tsp.toExcel(TSP_problem+"AntColony.xlsx")
    plt.close()

    tsp=AntSystem()
    tsp.readfile(fileName)
    tsp.gothrough(NC)
    tsp.toExcel(TSP_problem+"AntSystem.xlsx")
    plt.close()

