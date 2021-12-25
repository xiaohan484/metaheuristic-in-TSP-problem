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
class GA(TSP_Problem):
    def __init__(self):
        super().__init__()
    # nearestNeigbor needed
    # which slot
    def greedySearch(self,Road,n):
        cl=0
        Search=[i for i in np.arange(1,n)]
        L=0
        path=[0]
        for s in np.arange(1,n):
            q=random.random();
            Nearest=Search[np.argmin([Road[cl][i] for i in Search])]
            L+=Road[cl][Nearest]
            Search.remove(Nearest)
            path.append(Nearest)
            cl=Nearest
        path.append(0)
        L+=Road[cl][0]
        return path,L
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
            choice=random.choices(paths,k=2)
            
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
        t=0
        n=self.Xs.__len__()
        m=20 #population
        shortestPath=[]
        shortestLength=100000000
        fig=plt.figure()

        Change=False
        Road=np.array(self.Road,dtype=int)
        path1,L=self.greedySearch(self.Road,n)
        p=path1[1:len(path1)-1]
        paths=[path1.copy()]

        for i in np.arange(1,m):
            random.shuffle(p)
            path1[1:len(path1)-1]=p
            paths.append(path1.copy())
        

        time=timeit.default_timer()-time
        for t in np.arange(NC):
            stage1=timeit.default_timer()
            paths,gapath,gaLen=self.GA(paths)
            paths=paths[:m]
            gaLen=self.opt2_algorithm(gapath,gaLen)

            if shortestLength>gaLen:
                print('genetic Algorithm ---------------------------------------------------------------')
                shortestPath=gapath
                shortestLength=gaLen
                Change=True

            if(shortestLength!=self.LenPath(shortestPath)):
                print('Wrong After GA(*******************************************)')

            stage2=timeit.default_timer()
            self.draw(gapath,shortestPath)
            time+=stage2-stage1
            print('t: ',t)
            print('time: ',time)
            print('stage1-2',stage2-stage1)
            print(shortestLength)
            self.Time.append(time)
            self.solution.append(shortestLength)
    def print(self):
        print("t: ",self.t)


if __name__=='__main__':
    tsp=GA()
    tsp.readfile("xqf131.tsp")
    tsp.gothrough(100)

