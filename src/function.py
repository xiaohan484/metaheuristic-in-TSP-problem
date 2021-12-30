import numpy as np
import numba as nb
from numba import jit

def swap(List,indexA,indexB):
    temp=List[indexA]
    List[indexA]=List[indexB]
    List[indexB]=temp
def opt2Find(k,Road,path,pi_1,pi):
    pkp1=path[k+1]
    pk=path[k]
    link1=Road[pi_1][pi]+Road[pk][pkp1]
    link2=Road[pi_1][pk]+Road[pi][pkp1]
    return (link2<link1)

def LK_Update(path,Road,IndexList,n):
    plen=len(path)
    linkTour=[-1 for i in np.arange(n)]
    linkTourReversed=[-1 for i in np.arange(n)]

    start=0
    while(start<plen-1):
        #Step2
        t1=path[start]
        t2=path[start+1]

        #step 3
        for t3 in IndexList[t2]:
            if(yCannot[t2][t3]):
                continue
            g1=c(Road,[t1,t2])-c(Road,[t2,t3])
            if(g1>0):
                y.append([t2,t3])
                yCannot[t2][t3]=True
                yCannot[t3][t2]=True
                g.append(g1)
                G+=g1

        j=path.index(t3)
        k=0

        while(True):
            i=0
            #step 4
            Gstar=0
            G=g1
            x=[]
            y=[]
            x.append([t1,t2])
            xCannot[t1][t2]=False

            yCannot=[[False for i in np.arange(n)] for i in np.arange(n)]
            for i in np.arange(1,plen):
                yCannot[path[i-1]][path[i]]=True
                yCannot[path[i]][path[i-1]]=True
                linkTour[path[i-1]]=path[i]
                linkTourReversed[path[i]]=path[i-1]
            xCannot=[[False for i in np.arange(n)] for i in np.arange(n)]
            while(True):
                i=i+1
                t2i_1=path[j]
                t2i=path[j+1]
                xi=[t2i_1,t2i]
                yCannotHas.add(t2i)
                yCannotHas.add(t2i_1)
                for t in np.arange(IndexList[t2i]):
                    if(yCannot[t2i,t]):
                        continue
                    yi=[t2i,t]
                    gi=c(Road,xi)-c(Road,yi)
                    if(G+gi>0):
                        G+=gi
                        gistar=c(Road,xi)-c(Road,[t2i,t1])
                        if(G+gistart>Gistar):
                            Gistar=G+gistart
                            k=i
                        y.append([t2i,t])
                        yCannot[t2i][t]=True
                        yCannot[t][t2i]=True
                        j=path.index(t)
                        break
                if(G<=Gstar):
                    break
            if(Gstar>=0):
                #Step5
                for i in np.arange(k):
                    xi=x[i]
                    linkTour[xi[0]]=-1
                    linkTourReversed[xi[1]]=-1

                for i in np.arange(k):
                    yi=y[i]
                    linkTour[yi[0]]=yi[1]
                    lintTourReversed[yi[1]]=yi[0]

                check=1
                while(check<plen-1):
                    while(check<plen-1 and linkTour[path[check]]!=-1):
                        path[i]=linkTour[path[check-1]]
                    while(check<plen-1 and linkTourReversed[path[check]]!=-1):
                        path[i]=linkTourReversed[path[check-1]]
            else:
            #Step 6
                break #goto Step 4
def cost(Road,xi):
    return Road[xi[0]][xi[1]]



