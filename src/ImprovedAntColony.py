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
class ImprovedAntColony(TSP_Problem):
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
    def GA(self,paths):
        selectRatio=0.5
        end=paths.__len__()
        #CrossOverStep
        new=[]
        randomWeight=[1/self.LenPath(paths[i]) for i in np.arange(paths.__len__())]

        #CrossOver
        #Genetic Algorihm for Traveling Salesman Problem with Modified Cycle Crossover Operator
        index=[i for i in np.arange(paths.__len__())]
        remain=[i for i in np.arange(1,paths[0].__len__()-1)]
        pathRand=[i for i in np.arange(1,int(paths.__len__()/2))]
        for i in np.arange(0,end,2):
            choice=random.choices(paths,weights=randomWeight,k=2)
            
            p1=choice[0]
            p2=choice[1]

            P2=[False for i in np.arange(len(p1))]
            P2[0]=True
            P2[len(P2)-1]=True

            o1=p1.copy()
            o2=p2.copy()

            o1[1]=p2[1]
            P2[1]=True
            o2[1]=p2[p1.index(p2[p1.index(o1[1])])]

            for k in np.arange(2,len(p1)-1):
                if(P2[p1.index(o2[k-1])]==True):
                    j=P2.index(False)
                    o1[k]=p2[j]
                    P2[j]=True
                else:
                    o1[k]=p2[p1.index(o2[k-1])]
                    P2[p1.index(o2[k-1])]=True
                o2[k]=p2[p1.index(p2[p1.index(o1[k])])]
            new.append(o1)
            new.append(o2)

        for i in np.arange(0,end,2):
            r=random.sample(remain,k=2)
            r1,r2=r[0],r[1]
            p=paths[i].copy()
            p[r1],p[r2]=p[r2],p[r1]
            new.append(p)

        new.sort(key=lambda s:self.LenPath(s))
        Min=self.LenPath(new[0])
        minPath=new[0].copy()

        #paths=new
        #paths.extend(new)
        #paths.sort(key=lambda s:self.LenPath(s))

        return new,minPath,Min
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

        Tau0=1/n/self.greedySearch(self.Road,n)
        Tau=np.array([[Tau0 for i in np.arange(n)] for i in np.arange(n)])

        tour=np.arange(1,n)
        ant=np.arange(m)

        for k in np.arange(n):
            IndexList.append(allList.copy())
            IndexList[k].remove(k)


        time=timeit.default_timer()-time
        paths=[]
        lenOfpaths=[]
        support=[]
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



            for k in ant:
                if(tabu[k].__len__()<n+1):
                    print("Wrong",tabu[k].__len__())
                    continue
                Path=tabu[k]
                Lk=sum(Road[tabu[k][i-1]][tabu[k][i]] for i in np.arange(n+1))


                if currentShortestLength>Lk:
                    currentShortestPath=Path
                    currentShortestLength=Lk
                if t==0:
                    paths.append(Path)
                    lenOfpaths.append(Lk)
            Tau=(1-alpha)*Tau

            stageOpt=timeit.default_timer()
            currentShortestLength=self.opt2_algorithm(currentShortestPath,currentShortestLength)
            stageOpt=timeit.default_timer()-stageOpt



            if shortestLength>currentShortestLength:
                shortestPath=currentShortestPath
                shortestLength=currentShortestLength
                print('>>>>>>>>>>>>>>>>>>>>AntColony<<<<<<<<<<<<<<<<<<<<<,')
                support.append('antColony')

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
            paths,gaPath,gaLen=self.GA(paths)
            paths=paths[:m]
            gaLen=self.opt2_algorithm(gaPath,gaLen)

            if shortestLength>gaLen:
                shortestPath=gaPath
                shortestLength=gaLen
                print('--------------------GeneticAlgorithm---------------')
                support.append('GA')
            


            dTau=1/gaLen
            for i in np.arange(1,gaPath.__len__()):
                x,y=gaPath[i-1],gaPath[i]
                Tau[x][y]+=alpha*dTau
                Tau[y][x]+=alpha*dTau

            dTau=1/currentShortestLength
            for i in np.arange(1,currentShortestPath.__len__()):
                x,y=currentShortestPath[i-1],currentShortestPath[i]
                Tau[x][y]+=alpha*dTau
                Tau[y][x]+=alpha*dTau

            dTau=1/shortestLength
            for i in np.arange(1,shortestPath.__len__()):
                x,y=shortestPath[i-1],shortestPath[i]
                Tau[x][y]+=alpha*dTau
                Tau[y][x]+=alpha*dTau

            stage5=timeit.default_timer()
            if(t==0):
                Tau0=1/n/shortestLength
            self.draw(currentShortestPath,gaPath,shortestPath)
            stage6=timeit.default_timer()
            time+=stage5-stage1
            print('t: ',t)
            print('time: ',time)
            print('stage1-2',stage2-stage1)
            print('stage2-3',stage3-stage2)
            print('2opt:',stageOpt)
            print('stage3-4',stage4-stage3)
            print('stage4-5',stage5-stage4)
            print('plotTime:',stage6-stage5)
            print(shortestLength)
            self.Time.append(time)
            self.solution.append(shortestLength)
        print(support)





if __name__=='__main__':
    tsp=ImprovedAntColony()
    tsp.readfile("xqf131.tsp")
    tsp.gothrough(100)
    tsp.toExcel("test.xlsx")

