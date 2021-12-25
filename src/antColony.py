from openfile import TSP_Problem
from function import *
import numpy as np
import matplotlib.pyplot as plt
import random
import timeit
import copy
import collections
import pandas as pd
import sys
from datetime import datetime
import time

#alpha=1
#beta=1
#rho=0.5
#Q=100
class AntColony(TSP_Problem):
    def __init__(self):
        super().__init__()
    # nearestNeigbor needed
    # which slot
    def greedySearch(self,Road,n):
        cl=0
        Search=[i for i in np.arange(1,n)]
        L=0
        for s in np.arange(1,n):
            q=random.random();
            Nearest=Search[np.argmin([Road[cl][i] for i in Search])]
            L+=Road[cl][Nearest]
            Search.remove(Nearest)
            cl=Nearest
        L+=Road[cl][0]
        return L
    def SortNearestAdjacengList(self,List,Road):
        for i in np.arange(List.__len__()-1):
            Nearest=Road[i][i+1]
            NearestNeightbor=i+1
            for j in np.arange(i+2,List.__len__()):
                if(Road[i][j]< Road[i][NearestNeightbor]):
                    Nearest=Road[i][j]
                    NearestNeightbor=j
            List[i+1],List[NearestNeightbor]=List[NearestNeightbor],List[i+1]
    def LenPath(self,path):
        Lk=0
        for i in np.arange(1,path.__len__()):
            Lk+=self.Road[path[i-1]][path[i]]
        return Lk
    def gothrough(self,NC):
        time=timeit.default_timer()
        alpha=0.1
        rho=0.1
        beta=2
        phi=0.1
        t=0
        n=self.Xs.__len__()
        q0=0.95
        #Tau0=0.001

        m=20
        #m=self.Xs.__len__()
        antLocation=[]
        #place the m ants on the n nodes
        shortestPath=[]
        shortestLength=100000000


        initTabu=[]
        initNoneSearch=[]
        IndexList=[]
        allList=set(i for i in np.arange(n))


        Change=False
        Road=np.array(self.Road,dtype=int)
        allList=[i for i in np.arange(n)]
        self.SortNearestAdjacengList(allList,Road)
        Tau0=1/n/self.greedySearch(self.Road,n)
        
        Tau=np.array([[Tau0 for i in np.arange(n)] for i in np.arange(n)])

        tour=np.arange(1,n)
        ant=np.arange(m)

        time=timeit.default_timer()-time
        for k in np.arange(n):
            IndexList.append(allList.copy())
            IndexList[k].remove(k)


        for t in np.arange(NC):
            stage1=timeit.default_timer()
            random.seed(datetime.now())
            Probabilities=Tau/Road**beta
            s=0

            tabu=[]

            Start=random.randrange(n)
            for k in ant:
                tabu.append([i for i in np.arange(n+1)])
                tabu[k][0]=0
                tabu[k][n]=0

            stage2=timeit.default_timer()

            for k in ant:
                cl=tabu[k][0]
                #end=Search.__len__()
                for s in tour:
                    q=random.random();
                    Probability=Probabilities[cl][tabu[k][s:n]]
                    if q<q0 :
                        choiceIndex=np.argmax(Probability)
                    else:
                        r=np.argmax(Probability)
                        Probability[r]=0
                        choiceIndex=random.choices(np.arange(len(Probability)),weights=Probability,k=1)[0]
                    swap(tabu[k],s,s+choiceIndex)
                    choice=tabu[k][s]
                    Tau[cl][choice]=(1-rho)*Tau[cl][choice]+rho*Tau0
                    cl=choice



            stage3=timeit.default_timer()
            #Conclude results
            currentShortestLength=100000000
            currentShortestPath=[]

            paths=[]
            lenOfpaths=[]


            for k in ant:
                if(tabu[k].__len__()<n+1):
                    print("Wrong",tabu[k].__len__())
                    continue
                Path=tabu[k]
                Lk=sum(Road[tabu[k][i-1]][tabu[k][i]] for i in np.arange(n+1))


                if currentShortestLength>Lk:
                    currentShortestPath=Path
                    currentShortestLength=Lk
                paths.append(Path)
                lenOfpaths.append(Lk)
            Tau=(1-alpha)*Tau

            currentShortestLength=self.opt2_algorithm(currentShortestPath,currentShortestLength)

            dTau=1/currentShortestLength
            for i in np.arange(1,currentShortestPath.__len__()):
                x,y=currentShortestPath[i-1],currentShortestPath[i]
                Tau[x][y]+=alpha*dTau


            if shortestLength>currentShortestLength:
                shortestPath=currentShortestPath
                shortestLength=currentShortestLength
                print('>>>>>>>>>>>>>>>>>>>>AntColony<<<<<<<<<<<<<<<<<<<<<,')

            if(shortestLength!=self.LenPath(shortestPath)):
                print('Wrong Before GA(*******************************************)')


            paths.append(shortestPath)
            lenOfpaths.append(shortestLength)

            #dTau=1/shortestLength
            #for i in np.arange(1,shortestPath.__len__()):
            #    x,y=shortestPath[i-1],shortestPath[i]
            #    Tau[x][y]+=alpha*dTau
            #    Tau[y][x]+=alpha*dTau

            stage4=timeit.default_timer()

            if(shortestLength!=self.LenPath(shortestPath)):
                print('Wrong After GA(*******************************************)')

            self.draw(currentShortestPath,shortestPath)
            time+=stage4-stage1
            print('t: ',t)
            print('time: ',time)
            print('stage1-2',stage2-stage1)
            print('stage2-3',stage3-stage2)
            print('stage3-4',stage4-stage3)
            print(shortestLength)
            self.Time.append(time)
            self.solution.append(shortestLength)
    def print(self):
        print("t: ",self.t)



if __name__=='__main__':
    tsp=AntColony()
    #tsp.readfile("qa194.tsp")
    tsp.readfile("xqf131.tsp")
    tsp.gothrough(100)

