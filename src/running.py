from ImprovedAntColony import *
from ga import *
from antSystem import *
from antColony import *
from CooperativeAntColony2 import *
import matplotlib.pyplot as plt



if __name__=='__main__':
    TSP_problem="pbm436"
    NC=100
    fileName=TSP_problem+".tsp"
    
    for i in range(1,6):
        tsp=AntSystem()
        tsp.noDraw=True
        tsp.readfile(fileName)
        tsp.gothrough(NC)
        tsp.toExcel(TSP_problem+"AntSystem"+"exp"+str(i)+".xlsx")
        plt.close()

        tsp=CooperativeAntColony2()
        tsp.noDraw=True
        tsp.readfile(fileName)
        tsp.gothrough(NC)
        tsp.toExcel(TSP_problem+"CooperativeAntColony2"+"exp"+str(i)+".xlsx")
        plt.close()

        tsp=ImprovedAntColony()
        tsp.noDraw=True
        tsp.readfile(fileName)
        tsp.gothrough(NC)
        tsp.toExcel(TSP_problem+"ImprovedAntColony"+"exp"+str(i)+".xlsx")
        plt.close()

        tsp=GA()
        tsp.noDraw=True
        tsp.readfile(fileName)
        tsp.gothrough(NC)
        tsp.toExcel(TSP_problem+"GA"+"exp"+str(i)+".xlsx")
        plt.close()

        tsp=AntColony()
        tsp.noDraw=True
        tsp.readfile(fileName)
        tsp.gothrough(NC)
        tsp.toExcel(TSP_problem+"AntColony"+"exp"+str(i)+".xlsx")
        plt.close()


