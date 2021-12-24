from openfile import TSP_Problem
import matplotlib.pyplot as plt
import pulp
import numpy as np

class IntegerProgramming(TSP_Problem):
    def __init__(self):
        super().__init__()
    def modelerAndSolve(self):
        self.RoadChoice=[[pulp.LpVariable('e'+str(i)+'_'+str(j),0,1,cat='Binary') for j in np.arange(self.numOfRoad)] for i in np.arange(self.numOfRoad)]
        u=[pulp.LpVariable('u'+str(i),0,self.numOfRoad,cat='Integer') for i in np.arange(self.numOfRoad)]
        Obj=0

        Arange=np.arange(self.numOfRoad)
        offArange=np.arange(1,self.numOfRoad)
        for i in np.arange(self.numOfRoad):
            Obj+=pulp.lpSum(self.RoadChoice[i][j]*self.Road[i][j] for j in Arange[Arange!=i])

        model=pulp.LpProblem('TravellingSalemanProblem',pulp.LpMinimize)
        model+=Obj

        for i in np.arange(self.numOfRoad):
            model+=(pulp.lpSum([self.RoadChoice[i][j] for j in Arange[Arange!=i]])==1)
        for j in np.arange(self.numOfRoad):
            model+=(pulp.lpSum([self.RoadChoice[i][j] for i in Arange[Arange!=j]])==1)
            
        for i in np.arange(1,self.numOfRoad):
            for j in np.arange(1,self.numOfRoad):
                if(i==j):
                    continue
                model+= (u[i]-u[j]+self.numOfRoad*self.RoadChoice[i][j]<= self.numOfRoad-1)


        model.solve(pulp.PULP_CBC_CMD(threads=4,msg=True))
        print("objective Value:",pulp.value(Obj))


        plt.plot(self.Xs,self.Ys,'.')
        plt.xlabel('x-coordinate')
        plt.ylabel('y-coordinate')
        plt.axis('Equal')
        for i in np.arange(self.numOfRoad):
            for j in np.arange(self.numOfRoad):
                if(pulp.value(self.RoadChoice[i][j])==1):
                    plt.plot([self.Xs[i],self.Xs[j]],[self.Ys[i],self.Ys[j]],'-')
        plt.show()




if __name__=='__main__':
    tsp=IntegerProgramming()
    tsp.readfile("dj38.tsp")
    tsp.modelerAndSolve()
