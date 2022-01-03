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
    def initialize(self,m):
        Road=self.Road
        cluster=self.KmeanCluster()
        n=0
        pair=[]
        segmentPath=[]
        for i in np.arange(cluster.__len__()):
            if(cluster[i].__contains__(0)):
                swap(cluster,0,i)
                index=cluster[0].index(0)
                swap(cluster[0],index,0)
                break
        for c in cluster:
            tabu=[c[i] for i in np.arange(c.__len__())]
            n+=c.__len__()
            for cl in np.arange(0,c.__len__()-1):
                prob=[Road[c[cl]][c[k]] for k in np.arange(cl+1,c.__len__()-1)]
                if(len(prob)==0):
                    break
                choice=np.argmin(prob)
                choice+=cl+1
                swap(tabu,cl+1,choice)
            Lk=self.LenPath(tabu)
            Lk=self.opt2_algorithm(tabu,Lk)
            segmentPath.append(tabu)


        for i in np.arange(1,segmentPath.__len__()-1):
            endPoint=segmentPath[i][-1]
            pathResult=[self.pathDistance(endPoint,segmentPath[j],Road) for j in np.arange(i+1,segmentPath.__len__()-1)]
            if(pathResult.__len__()==0):
                break
            choice=np.argmin(pathResult)
            choice+=i+1
            swap(segmentPath,i,choice)


        path=[0 for i in np.arange(n+1)]
        c=0
        for p in segmentPath:
            path[c:p.__len__()+c]=p
            c+=p.__len__()
        path[-1]=path[0]
        for i in np.arange(1,len(path)):
            p1=path[i]
            p2=path[i-1]
        Lk=self.LenPath(path)
        Lk=self.opt2_algorithm(path,Lk)

        pa=segmentPath[1:]
        paths=[path]


        for i in np.arange(m-1):
            random.shuffle(pa)
            pathGen=[0 for i in np.arange(n+1)]
            pathGen[:segmentPath[0].__len__()]=segmentPath[0]
            c=segmentPath[0].__len__()
            for p in pa:
                pathGen[c:p.__len__()+c]=p
                c+=p.__len__()
            pathGen[-1]=pathGen[0]
            paths.append(pathGen.copy())

        return paths,path,Lk

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
    def pathDistance(self,endPoint,path,Road):
        p1=path[0]
        p2=path[-1]
        d1=Road[endPoint][p1]
        d2=Road[endPoint][p2]
        if(d2<d1):
            path.reverse()
        return min(d1,d2)
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
        path,L2=self.greedySearch(Road,n)
        paths=[]
        paths.append(path)
        
        p2=path[1:len(path)-1]


        for i in np.arange(1,m/2):
            random.shuffle(p2)
            path[1:len(path)-1]=p2
            paths.append(path.copy())
        

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
    tsp.readfile("pbm436.tsp")
    tsp.gothrough(100)

