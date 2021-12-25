import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import random
import time
#member 
class TSP_Problem:
    def __init__(self):
        self.Xs=[]
        self.Ys=[]
        self.Road=[]
        self.numOfRoad=0
        self.Time=[]
        self.solution=[]
        self.fig=plt.figure()
    def IterInformation(self):
        return self.Time,self.solution
    def LenPath(self,path):
        Lk=0
        for i in np.arange(1,path.__len__()):
            Lk+=self.Road[path[i-1]][path[i]]
        return Lk
    def readfile(self,filename):
        curPath=os.path.dirname(__file__)
        newPath=os.path.relpath('../tsp/'+filename,curPath)
        with open(newPath) as file:
            des,name=file.readline().split(': ')
            read=file.readline()
            while(read!='NODE_COORD_SECTION\n'):
                read=file.readline()

            Buffer=file.readline()
            while(Buffer[0].isnumeric()):
                num,x,y=Buffer.split(' ')
                num=int(num)
                x=float(x)
                y=float(y)
                self.Xs.append(x)
                self.Ys.append(y)
                Buffer=file.readline()
            self.linkRoad()
    def opt2_algorithm(self,path,Lk):
        bestDistance=Lk
        len=path.__len__()-1
        Break=False

        Road=self.Road
        iLen=np.arange(1,len)
        while(True):
            for i in iLen:
                pi_1=path[i-1]
                pi=path[i]
                for k in np.arange(i+1,len):
                    pkp1=path[k+1]
                    pk=path[k]
                    link1=Road[pi_1][pi]+Road[pk][pkp1]
                    link2=Road[pi_1][pk]+Road[pi][pkp1]
                    if(link2<link1):
                        Lk+=-link1+link2
                        path[i:k+1]=reversed(path[i:k+1])
                        pi_1=path[i-1]
                        pi=path[i]
            #print(Lk)
            if(bestDistance>Lk):
                bestDistance=Lk
            else:
                break
        return Lk
    def opt3_algorithm(self,path,Lk):
        bestDistance=Lk
        len=path.__len__()-1
        Break=False
        Road=self.Road
        iLen=np.arange(1,len)

        while(True):
            for i in iLen:
                nodeA=i-1
                nodeB=i
                pa=path[nodeA]
                pb=path[nodeB]
                for j in np.arange(i+1,len):
                    nodeC=j
                    nodeD=j+1
                    pc=path[nodeC]
                    pd=path[nodeD]
                    for k in np.arange(j+2,len):
                        nodeE=k
                        nodeF=k+1
                        pe=path[nodeE]
                        pf=path[nodeF]

                        d0=Road[pa][pb]+Road[pc][pd]+Road[pe][pf]
                        d=[Road[pa][pc]+Road[pb][pe]+Road[pd][pf],\
                        Road[pa][pd]+Road[pe][pb]+Road[pc][pf],\
                        Road[pa][pd]+Road[pe][pc]+Road[pb][pf],\
                        Road[pa][pe]+Road[pd][pb]+Road[pc][pf],\
                        Road[pa][pb]+Road[pc][pe]+Road[pd][pf],\
                        Road[pa][pc]+Road[pb][pd]+Road[pe][pf],\
                        Road[pa][pe]+Road[pd][pc]+Road[pb][pf],\
                        ]
                        choice=np.argmin(d)

                        if(d[choice]>d0):
                            continue
                        else:
                            if(choice==0):
                                path[nodeB:nodeE+1]=list(reversed(path[nodeB:nodeC+1]))+list(reversed(path[nodeD:nodeE+1]))
                            elif(choice==1):
                                path[nodeB:nodeE+1]=path[nodeD:nodeE+1]+path[nodeB:nodeC+1]
                            elif(choice==2):
                                path[nodeB:nodeE+1]=path[nodeD:nodeE+1]+list(reversed(path[nodeB:nodeC+1]))
                            elif(choice==3):
                                path[nodeB:nodeE+1]=list(reversed(path[nodeD:nodeE+1]))+path[nodeB:nodeC+1]
                            elif(choice==4):
                                path[nodeD:nodeE+1]=reversed(path[nodeD:nodeE+1])
                            elif(choice==5):
                                path[nodeB:nodeC+1]=reversed(path[nodeB:nodeC+1])
                            elif(choice==6):
                                path[nodeB:nodeE+1]=reversed(path[nodeB:nodeE+1])

                            

                            Lk+=-d0+d[choice]
                            pa=path[nodeA]
                            pb=path[nodeB]
                            pc=path[nodeC]
                            pd=path[nodeD]
                            if(Lk!=self.LenPath(path)):
                                print('something Wrong------------------------------------')
                                print(Lk,' ',self.LenPath(path),' ',d0,' ',d[choice])
                                sys.exit()
                            #Break=True
                            #break
                    #if(Break):
                    #    break
            Break=False
            if(bestDistance>Lk):
                bestDistance=Lk
            else:
                break
        return Lk
    def show(self):
        plt.plot(self.Xs,self.Ys,'.')
        plt.xlabel('x-coordinate')
        plt.ylabel('y-coordinate')
    def linkRoad(self):
        self.numOfRoad=self.Xs.__len__()
        #self.Road=np.zeros((self.numOfRoad,self.numOfRoad),int)
        n=self.numOfRoad
        self.Road=[[0 for i in range(n)] for j in range(n)]
        for i in range(n):
            Xi=self.Xs[i]
            Yi=self.Ys[i]
            for j in range(n):
                x=Xi-self.Xs[j]
                y=Yi-self.Ys[j]
                self.Road[i][j]=(np.round(np.sqrt(x*x+y*y)))
    def draw(self,*paths):
        return 
        plt.clf()
        plt.subplot(2,1,1)
        plt.xlabel('x-coordinate')
        plt.ylabel('y-coordinate')
        plt.axis('Equal')
        plt.plot(self.Xs,self.Ys,'g.')
        for i in np.arange(paths.__len__()):
            if i==paths.__len__()-1:
                color='b'
            elif i==paths.__len__()-2:
                color='r'
            elif i==paths.__len__()-3:
                color='g'
            plt.plot([self.Xs[j] for j in paths[i]],[self.Ys[j] for j in paths[i]],color+'-')
        self.drawTime()
        self.fig.canvas.flush_events()
        plt.pause(0.001)
    def drawTime(self):
        plt.subplot(2,1,2)
        plt.xlabel('time(s)')
        plt.ylabel('tour length(m)')
        plt.plot(self.Time,self.solution,'b-')
    def toExcel(self,filename):
        data=pd.DataFrame()
        data['iteration']=range(1,self.Time.__len__()+1)
        data['Time(seconds)']=self.Time
        data['shortest length']=self.solution

        curPath=os.path.dirname(__file__)
        filePath=os.path.relpath('../Excel/'+filename,curPath)
        data.to_excel(filePath,sheet_name=filename)
    def KmeanCluster(self):
        k=int(round(np.sqrt(len(self.Xs))+0.5))
        seed=[]

        s=random.sample([i for i in range(len(self.Xs))],k)
        for i in range(k):
            seed.append([self.Xs[s[i]],self.Ys[s[i]]])

        Cluster=[[None] for j in range(k)]
        countNotChange=0

        while(countNotChange<k):
            countNotChange=0
            for j in range(k):
                Cluster[j].clear()
            # Clustering
            for i in range(len(self.Xs)):
                x=self.Xs[i]
                y=self.Ys[i]
                Min=min(seed,key=lambda s:np.sqrt((s[0]-x)**2+(s[1]-y)**2))
                Cluster[seed.index(Min)].append(i)
            #seed Update
            for j in range(k):
                s=[0,0]
                for p in Cluster[j]:
                    s[0]+=self.Xs[p]
                    s[1]+=self.Ys[p]
                if(Cluster[j].__len__()!=0):
                    s[0]/=Cluster[j].__len__()
                    s[1]/=Cluster[j].__len__()
                    if(np.sqrt((seed[j][0]-s[0])**2+(seed[j][0]-s[0])**2)<0.5):
                        countNotChange+=1
                    seed[j]=s
            plt.clf()
            for p in Cluster:
                plt.plot([self.Xs[i] for i in p],[self.Ys[i] for i in p],'.')
            plt.gca().set_prop_cycle(None)
            for p in seed:
                plt.plot(p[0] ,p[1],'o',ms=10)
            self.fig.canvas.flush_events()
            plt.pause(0.001)
        return Cluster
        
if __name__=='__main__':
    tsp= TSP_Problem()
    tsp.readfile('qa194.tsp')
    tsp.KmeanCluster()





