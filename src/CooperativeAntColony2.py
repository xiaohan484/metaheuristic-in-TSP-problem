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
import collections as co

#alpha=1Y:
#beta=1Y:
#rho=0.5Y:
#Q=100Y9
class ImprovedAntColony(TSP_Problem):
    def __init__(self):
        super().__init__()
    def Lin_Kernighan(self,path):
        Road=self.Road
        len=path.__len__()-1
        iLen=np.arange(0,len-1,1)
        shortest=path.copy()
        Lk=self.LenPath(path)
        originalL=Lk
        delete=[]
        pk=-1
        k=-1
        bestDistance=Lk
        while(1):
            for i in iLen:
                key=path[1]
                path[:len]=path[1:]
                path[-1]=key
                pi=path[0]
                pi1=path[1]
                k=-1
                count=0
                for j in range(2,len):
                    Gi=0
                    Giopt=0
                    pj=path[j]
                    pj1=path[j+1]
                    gi=Road[pi][pi1]-Road[pi1][pj1]
                    gis=Road[pj][pj1]-Road[pi][pj]
                    if(gi+gis>0 or gi>0):
                        template=path.copy()
                        template[1:j+1]=template[j:0:-1]#reversed(template[1:j+1])
                        if(gi+gis>0):
                            shortest=template.copy()
                            Giopt=gi+gis
                            #s=self.LenPath(shortest)
                            #if(s!=self.LenPath(path)-(gi+gis)):
                            #    sys.exit()
                        Gi+=gi
                        k=j
                        while j<len:
                            pj=path[j]
                            pj1=path[j+1]
                            pk=path[k]
                            pk1=path[k+1]
                            gi =Road[pk][pk1]-Road[pk][pj1]
                            gis=Road[pj][pj1]-Road[pi][pj]
                            if(gi>0):
                                template[1:j+1]=template[j:0:-1]#reversed(template[1:j+1])
                                #template[1:j+1]=reversed(template[1:j+1])
                                Gi+=gi
                                if(Gi+gis>Giopt):
                                    shortest=template.copy()
                                    Giopt=Gi+gis
                                    #s=self.LenPath(shortest)
                                    #if(s!=self.LenPath(path)-(Gi+gis)):
                                    #    sys.exit()
                                k=j
                                j+=2
                            else:
                                j+=1
                        if(Giopt>0):
                            path[:]=shortest[:]
                            break
            if(bestDistance>self.LenPath(shortest)):
                bestDistance=self.LenPath(shortest)
            else:
                break
        i=path.index(0)
        key=path[i]
        path[:]=list(path[i:])+list(path[1:i+1])
        path[-1]=key
        Lk=self.LenPath(path)
        if(Lk>originalL):
            sys.exit()
        return Lk
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
    def crossOver(self,paths):
        end=round(paths.__len__()/2)
        new=[None for i in np.arange(end)]
        index=[i for i in np.arange(paths.__len__())]
        remain=[i for i in np.arange(1,paths[0].__len__()-1)]
        pathRand=[i for i in np.arange(1,int(paths.__len__()/2))]
        st=timeit.default_timer()
        for i in np.arange(end):
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
            new[2*i]=o1
            new[2*i+1]=o2
        return new
    def GA(self,paths):
        selectRatio=0.5
        end=round(paths.__len__()/2)
        #CrossOverStep
        new=[None for i in np.arange(2*end)]
        randomWeight=[1/self.LenPath(paths[i]) for i in np.arange(paths.__len__())]

        #CrossOver
        #Genetic Algorihm for Traveling Salesman Problem with Modified Cycle Crossover Operator
        index=[i for i in np.arange(paths.__len__())]
        remain=[i for i in np.arange(1,paths[0].__len__()-1)]
        pathRand=[i for i in np.arange(1,int(paths.__len__()/2))]
        st=timeit.default_timer()
        for i in np.arange(end):
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
            new[2*i]=o1
            new[2*i+1]=o2


        #mutual First
        new2=[None for i in np.arange(0,end)]
        for i in np.arange(0,end):
            #p=paths[i].copy()
            r=random.sample(remain,k=2)
            r1,r2=r[0],r[1]
            p=paths[i].copy()
            p[r1],p[r2]=p[r2],p[r1]
            new2[i]=p
        new.extend(new2)
        #mutual Second




        new.sort(key=lambda s:self.LenPath(s))
        Min=self.LenPath(new[0])
        minPath=new[0].copy()

        #paths=new
        #paths.extend(new)
        #paths.sort(key=lambda s:self.LenPath(s))

        return new,minPath,Min
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
        allList=[i for i in np.arange(n)]
        Change=False

        Road=np.array(self.Road,dtype=int)
        allList=[i for i in np.arange(n)]

        for i in np.arange(n):
            IndexList.append(list(filter(lambda s:s!=i,allList)))
            IndexList[i].sort(key=lambda s:Road[i][s])

        Q=1
        Tau0=Q/n/self.greedySearch(self.Road,n)
        Tau=np.array([[Tau0 for i in np.arange(n)] for i in np.arange(n)])

        tour=np.arange(1,n)
        ant=np.arange(m)



        time=timeit.default_timer()-time
        paths=[]
        lenOfpaths=[]
        support=[]
        Em=-((n-1)*np.log(1/(n-1)))
        probe=np.zeros((n,n),float)
        A=1
        Tmin=0
        Probabilities=(Tau**A)/(Road**beta)
        eta=1/Road
        #Probabilities=1/(Road**beta)
        pdec=0.05 ** (1/(n-1))
        for t in np.arange(NC):
            stage1=timeit.default_timer()
            #Tmax=np.max(Tau)
            #Tmin=(Tmax)*(1-pdec)/(n/2)/pdec
            #Tau[Tau<Tau0/10]=Tau0/10
            #Tau[Tau<Tmin]=Tmin

            probe/=20
            E=-np.sum([p*np.log(p) for p in probe[probe>0]])
            if(t==0):
                Ep=1
            else:
                Ep=E/Em


            Probabilities=Tau**A/Road**beta
            probe=np.zeros((n,n),float)


            s=0

            tabu=[]
            ptabu=[]

            Start=random.randrange(n)
            for k in ant:
                tabu.append([i for i in np.arange(n+1)])
                tabu[k][0]=0
                tabu[k][n]=0

            stage2=timeit.default_timer()

            if(t==0):
                for k in range(round(m/2)):
                    for i in range(1,len(shortestPath)):
                        cl=shortestPath[i]
                        inject=random.choices(np.arange(len(eta)),weights=eta[cl],k=10)
                        if(choiceIndex in inject):
                            inject.remove(choiceIndex)
                            Tau[choice][cl]=(1-rho)*Tau[choice][cl]+rho*Tau0*Q
                            Tau[cl][choice]=(1-rho)*Tau[cl][choice]+rho*Tau0*Q

            for k in ant:
                cl=tabu[k][0]
                for s in tour:
                    q=random.random();
                    Probability=Probabilities[cl][tabu[k][s:min(s+round(n/4),n)]]
                    if q<q0 :
                        choiceIndex=np.argmax(Probability)
                        r=np.argmax(Probability)
                        Probability[r]=0
                    else:
                        r=np.argmax(Probability)
                        Probability[r]=0
                        choiceIndex=random.choices(np.arange(len(Probability)),weights=Probability,k=1)[0]
                    #inject
                    swap(tabu[k],s,s+choiceIndex)
                    choice=tabu[k][s]
                    cl=choice
                for i in range(1,len(tabu[k])):
                    x=tabu[k][i-1]
                    y=tabu[k][i]
                    Tau[x][y]=(1-rho)*Tau[x][y]+rho*Tau0*Q









            #Conclude results
            currentShortestLength=100000000
            bestsofar=0
            currentShortestPath=[]




            state=0
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

            stage3=timeit.default_timer()
            currentShortestLength=self.Lin_Kernighan(currentShortestPath)
            #currentShortestLength=self.opt2_algorithm(currentShortestPath,currentShortestLength)
            Change=False


            if shortestLength>currentShortestLength:
                shortestPath=currentShortestPath
                shortestLength=currentShortestLength
                Change=True
                print('>>>>>>>>>>>>>>>>>>>AntColony<<<<<<<<<<<<<<<<<<<<<,')
                support.append('antColony ')

            if(shortestLength!=self.LenPath(shortestPath)):
                print(shortestLength,' ',self.LenPath(shortestPath))
                print('Wrong Before GA(*******************************************)')
                sys.exit()

        
            stage4=timeit.default_timer()
            paths.append(shortestPath)

            paths,gaPath,gaLen=self.GA(paths)
            paths=paths[:m]
            gaLen=self.Lin_Kernighan(gaPath)
            #gaLen=self.opt2_algorithm(gaPath,gaLen)
            stage5=timeit.default_timer()


            if shortestLength>gaLen:
                shortestPath=gaPath
                shortestLength=gaLen
                Change=True
                print('--------------------GeneticAlgorithm---------------')
                support.append('GA')

            

            dTau=Q/gaLen
            for i in np.arange(1,gaPath.__len__()):
                x,y=gaPath[i-1],gaPath[i]
                Tau[x][y]+=alpha*dTau
                Tau[y][x]+=alpha*dTau

            dTau=Q/currentShortestLength
            for i in np.arange(1,currentShortestPath.__len__()):
                x,y=currentShortestPath[i-1],currentShortestPath[i]
                Tau[x][y]+=alpha*dTau
                Tau[y][x]+=alpha*dTau

            dTau=Q/shortestLength
            for i in np.arange(1,shortestPath.__len__()):
                x,y=shortestPath[i-1],shortestPath[i]
                Tau[x][y]+=alpha*dTau
                Tau[y][x]+=alpha*dTau


            #random close
            #i=random.randint(1,n)
            #x,y=shortestPath[i-1],shortestPath[i]
            #Tau[x][y]=0

            stage6=timeit.default_timer()
            if(t==0):
                Tau0=1/n/shortestLength
            self.draw(currentShortestPath,gaPath,shortestPath)
            stage7=timeit.default_timer()
            time+=stage6-stage1
            print('t: ',t)
            print('time: ',time)
            print('stage1-2',stage2-stage1)
            print('stage2-3',stage3-stage2)
            print('stage3-4',stage4-stage3)
            print('stage4-5',stage5-stage4)
            print('stage5-6',stage6-stage5)
            print('plotTime:',stage7-stage6)
            print(shortestLength)
            self.Time.append(time)
            self.solution.append(shortestLength)
        print(support)





if __name__=='__main__':
    tsp=ImprovedAntColony()
    tsp.readfile("xqf131.tsp")
    tsp.gothrough(100)
    tsp.toExcel("test.xlsx")

