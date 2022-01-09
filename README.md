# Traveling Salesman Problem(TSP)
Traveling Salesman Problem is an NP-hard problem in combinatorial optimization problem in operations researchs.

>Given:
>- A list of cities
>- Between each pair of cities

>Question:
>- What is the shortest possible route that visits all city?

>Constraint:
>- Each city exactly be visited once
>- Return to the origin city finally

## TSP Solving Algorithm

1. Integer Linear programming formulation(Exact solution)
    - Miller-Tucker-Zemlin formulation
    - Dantzig-Fulkerson-Johnson formulation
2. Heristic/meta-heuristic algorithm(approximate solution)
    1. Heuristic
        - k-opt algorithm
        - Lin-Kernighan heuristic
    3. Meta-heuristic
        - Randomized algorithm
        - Genetic algorithm
        - Ant Colony System

## Current best technique for TSP solving
#### Concorde TSP Solver
Concorde TSP solver is program for TSP problem.That using Cutting plane method(Dantzig-Fulkerson-Johnson formulation)  to solve the TSP problem. 

#### Lin-kernighan Heristics
Best heuristic for symmetric travelling salesman problem.The algorithm's idea is decide to choose two set links(removals links and additional links) in all set links to reduce the tour length. 

Similar algorithms a k-opt algorithm(2-opt,3-opt algorithm):
- Given a  in TSP, Switching(removing and adding) k link to improve the current solution.

#### Meta-heuristic algorithm
- Ant Colony algorithm
- Genetic algorithm
- Shuffle frog leaping algorithm
- Particle swap algorithm
- Simulated annealing

## Cooperative genetic ant system
<img src="https://user-images.githubusercontent.com/72375847/148684181-59af771e-699f-46b1-9a58-b7d8e42995e8.png" width=10% height=10%>

### Ant Colony System part
Ant Colony System simmulate the real ant colony's behaviour to solve the TSP. In the ant's behaviour:
1. When an ant go across some path in tour,it will  drop some pheromone in the path.
2. Other ants mostly choose the path that has the pheromone from their team.
3. Finally, the ants will always using some paths to find food.

#### The probability of Ant decide path:
<img src="https://user-images.githubusercontent.com/72375847/148683380-d8b12b94-187d-4e15-a294-1baba02a1c37.png" width=30 height=30> 

probability to choose the maximum pheromone in the path.

<img src="https://user-images.githubusercontent.com/72375847/148683374-0a9c8009-07fd-423a-8135-4027d78e53bc.png" width=40% height=40%> 

Using the pheromone factor to chose the path.

<img src="https://user-images.githubusercontent.com/72375847/148683431-a5c91eab-03a0-48c0-8351-f991b8c0a853.png" width=40% height=40%> 

```python=
Probabilities=Tau/Road**beta
...
...#choose next city
if q<q0 :
    choiceIndex=np.argmax(Probability)
else:
    r=np.argmax(Probability)
    Probability[r]=0
choiceIndex=random.choices(np.arange(len(Probability)),weights=Probability,k=1)[0]
```
#### Pheromone Global Updating Rule:
Using the best history solution to update pheromone, the ants will study best solution in next iteration.
<img src="https://user-images.githubusercontent.com/72375847/148683444-7bd13e84-089d-4e5c-8399-3b627a6b11d2.png" width=40% height=40%> 

```python=
 dTau=1/shortestLength
    for i in np.arange(1,shortestPath.__len__()):
        x,y=shortestPath[i-1],shortestPath[i] # for all choice in shortest path
        Tau[x][y]+=alpha*dTau# update pheromone
        Tau[y][x]+=alpha*dTau
```
#### Local Updating Rule:
Change behaviour of the current iteration, let next ant will study the ant solution before
<img src="https://user-images.githubusercontent.com/72375847/148683438-5dfec035-481f-47bf-b475-c81e8fb1281c.png" width=40% height=40%>

```python=
...#when choose a city, update local pheremone immediately
Tau[cl][choice]=(1-rho)*Tau[cl][choice]+rho*Tau0
```
#### Settings

<img src="https://user-images.githubusercontent.com/72375847/148683450-6e57e991-4298-468c-8a9f-c50734fb3eb3.png" width=20% height=20%> 

### Genetic algorithm part
Genetic algorithm is the idea's that is using the good solutions to produce next generation solutions to find better solutions.
That properly has 3 step:
1. selection
    - Choose the good solutions in solution set.
2. Crossover
    - Combine the solution from good solution set to make new solutions.
3. Mutation
    - slightly change current solution to make new solution
Genetic algorithm belive the better solution can be make from good solutions or slightly changing in good solution.

In Our algorithm,
1. [Cycle Crossover Operator(CX2)](https://www.hindawi.com/journals/cin/2017/7430125/)
    1. Select 1st bit from second parent as 1st bit of offspring
    2.
        - Find the bit from step 2 in first parent
        - Pick the exact same position bit in second parent
        - Find the bit in First parent
        - Select the exact same position bit which is in second parent
    3.  
        - Selected bit from Step 3 can be found in first parent
        -  pick the exact same position bit which is in second parent as the next bit for first offspring
    4. Repeat step 2-3 untill 1st bit of first parent will not come in second offspring
    5. If some bits are left, Repeating step 1-4 otherwise the algorithm end.
```python=
o1[1]=p2[1]# Step 1 O is the child and p is parent
P2[1]=True# P is checker that check the city is in child
o2[1]=p2[p1.index(p2[p1.index(o1[1])])]

for k in np.arange(2,len(p1)-1):#step 2-4
    if(P2[p1.index(o2[k-1])]==True):#step 5 if some bits are left
        j=P2.index(False)
        o1[k]=p2[j]
        P2[j]=True
    else:
        o1[k]=p2[p1.index(o2[k-1])]
        P2[p1.index(o2[k-1])]=True
    o2[k]=p2[p1.index(p2[p1.index(o1[k])])]
```
<img src="https://user-images.githubusercontent.com/72375847/148683495-80657315-4403-435c-8e1e-424ee16efcd0.gif" width=50% height=50%> 

2. [Mutation operator](https://ieeexplore.ieee.org/abstract/document/4370274)
    1. Random select two city
    2. Exchange the two city order
```python=
for i in np.arange(0,end,2):
    r=random.sample(remain,k=2)
    r1,r2=r[0],r[1]
    p=paths[i].copy()
    p[r1],p[r2]=p[r2],p[r1]
    new.append(p)
```
<img src="https://user-images.githubusercontent.com/72375847/148683506-23fa47fb-cef7-4f7c-a2e0-ef940d80cadc.gif" width=50% height=50%> 

## Local Search
### 2-opt algorithm
2-opt algorithm is quite easy, the idea's is switch two link to improve solution.

```python=
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
                #when swich two link, the path between
                #two link will reversed in order
                pi_1=path[i-1]
                pi=path[i]
    #print(Lk)
    if(bestDistance>Lk):
        bestDistance=Lk
    else:
        break
```
<img src="https://user-images.githubusercontent.com/72375847/148683989-820474ff-1158-442b-b638-8916adc779f6.gif" width=50% height=50%> 

### Lin-Kernighan algorithm
Simple Description:
1. Choose a link that will be remove
```python=
for i in iLen:
            key=path[1]
            path[:len]=path[1:]
            path[-1]=key
            pi=path[0]
            pi1=path[1]
            k=-1
            count=0
```
2. chooce another link that added can reduce the tour length
```python=
for j in range(2,len):
    Gi=0
    Giopt=0
    pj=path[j]
    pj1=path[j+1]
    gi=Road[pi][pi1]-Road[pi1][pj1]
    gis=Road[pj][pj1]-Road[pi][pj]
    if(gi+gis>0 or gi>0):#if possible improve
        template=path.copy()
        template[1:j+1]=template[j:0:-1
        if(gi+gis>0):
            shortest=template.copy()#save the result
            Giopt=gi+gis
        Gi+=gi
        k=j
```

3. Repeat remove link and add link until check all possible link
```python=
 while j<len:#remove k- k+1 and add j- j+1 link
        pj=path[j]
        pj1=path[j+1]
        pk=path[k]
        pk1=path[k+1]
        gi =Road[pk][pk1]-Road[pk][pj1]
        gis=Road[pj][pj1]-Road[pi][pj]
        if(gi>0):#If possible improve
            template[1:j+1]=template[j:0:-1]
            Gi+=gi
            if(Gi+gis>Giopt): # store the best result
                shortest=template.copy()
                Giopt=Gi+gis
            k=j
            j+=2
        else:
            j+=1
    if(Giopt>0):
        path[:]=shortest[:]# use the best result replace paths
        break
```
4. check any improve,if has any improve repeat the process 1-3
```python=
if(bestDistance>self.LenPath(shortest)):
                bestDistance=self.LenPath(shortest)
            else:
                break
```
<img src="https://user-images.githubusercontent.com/72375847/148683980-499ab33c-b8ed-437e-8b29-b2af73a1a2b3.gif" width=50% height=50%> 

## Reference
[Traveling Salesman Problem   -wikipedia](https://en.wikipedia.org/wiki/Travelling_salesman_problem)

[Concorde TSP Solver   -wikipedia](https://en.wikipedia.org/wiki/Concorde_TSP_Solver)

[Concorde Home](https://www.math.uwaterloo.ca/tsp/concorde.html)

[Ant Colony Sytem](https://ieeexplore.ieee.org/abstract/document/585892)

[Genetic Algorithm for Traveling Salesman Problem with Modified Cycle Crossover Operator](https://www.hindawi.com/journals/cin/2017/7430125/)

[An Improved Genetic Algorithm for TSP](https://ieeexplore.ieee.org/abstract/document/4370274)

[Data Structures for Traveling Salesmen](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.49.570&rep=rep1&type=pdf)
