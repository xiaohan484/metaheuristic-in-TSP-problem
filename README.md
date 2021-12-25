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
### Concorde TSP Solver
Concorde TSP solver is program for TSP problem.That using Cutting plane method(Dantzig-Fulkerson-Johnson formulation)  to solve the TSP problem. In Concorde introduction,

Dantzig-Fulkerson-Johnson :
For every set $S$ of cities
$x(S)=\sum(x_e:e\subseteq S)$

For every choice of disjoint sets $S,T$
$x(S,T)=\sum(x_e:e\cap S\neq \emptyset,e \cap T \neq \emptyset)$

Constraint:
each $x$ in $S$ satisfies
$0\leq x_e\leq1 \text{    for all edges e}$

$x(\{v\},V-\{v\})=2$

Subtour elimination constrains
$x(S,V-S)\geq 2$


### Lin-kernighan Heristics
Best heuristic for symmetric travelling salesman problem.The algorithm's idea is decide to choose two set links(removals links and additional links) in all set links to reduce the tour length. 

Similar algorithms a k-opt algorithm(2-opt,3-opt algorithm):
- Given a  in TSP, Switching(removing and adding) k link to improve the current solution.

## Our algorithm
Our algorithm's idea is from .[Cooperative genetic ant system](https://www.sciencedirect.com/science/article/pii/S0957417411014977)
Using different technique from Genetic and Ant Colony system to find the better solution, and the technique will provide its best solution to other technique for improved solution later.
```
Initialize parameters(pheremone)
Construct First solution sets from Ant Colony System
Initialize GA from First solution set
While iter < max iterations do
    Construct NewAntSolutions(NAS) from Ant Colony System
    input the best solution to GA if NAS make the solution improved 
    Construct NewAntGeneration(NAG) by GA
    Refine Solution by 2-opt algorithm from NAS and NAG best solution
    Select NewBestSolution set from NAS and NAG
    Global Update Pheromones(using Best solution in history,NAS,NAG)
endwhile
output the best solution in history
```
But we using ant colony system and other genetic operators.

### Ant Colony System part
Ant Colony System simmulate the real ant colony's behaviour to solve the TSP. In the ant's behaviour:
1. When an ant go across some path in tour,it will  drop some pheromone in the path.
2. Other ants mostly choose the path that has the pheromone from their team.
3. Finally, the ants will always using some paths to find food.
#### The probability of Ant decide path:
$q_0$ probability to choose the maximum pheromone in the path.
$s=\begin{cases}
arg max_{u\in J_k(r)}{\tau(r,u)\cdot\eta^\beta(r,u)}, \text{if} q\leq q_0\\
S,&otherwise(next equation)
\end{cases}$
Using the pheromone factor to chose the path.
$p_k(r,s)=\begin{cases}
\dfrac{\tau(r,s)\cdot\eta^\beta(r,s)}{\sum_{u\in J_k(r)}\tau(r,u)\eta^\beta(r,s)} \\
0, &\text{otherwise}
\end{cases}$

#### Pheromone Global Updating Rule:
Using the best history solution to update pheromone, the ants will study best solution in next iteration.
$\tau(r,s)\leftarrow(1-\alpha)\cdot\tau(r,s)+\sum_{k=1}^m\Delta\tau(r,s)$
$\Delta\tau=\dfrac{1}{L_{gb}}, L_{gb}=\text{tour length in best solution}$
#### Local Updating Rule:
Change behaviour of the current iteration, let next ant will study the ant solution before
$\tau(r,s)\leftarrow(1-\rho)\cdot\tau(r,s)+\rho\cdot\Delta\tau(r,s)$
#### Settings
- $\alpha=0.1$
- $\rho=0.1$
- $\beta=2$
- $q_0=0.9$
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
2. [Mutation operator](https://ieeexplore.ieee.org/abstract/document/4370274)
    1. Random select two city
    2. Exchange the two city order
### Solution Refinement(2-opt algorithm)
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
## Result
Comparison:
- Ant System + 2-opt
- Ant Colony System + 2-opt
- Genetic algorithm + 2-opt
- our algorithm(Ant Colony System + Genetic algorithm+ 2-opt)
Other technique:
- Concorde TSP Solver
- Integer Programming- Miller Tucker Zemlin Formulation

[TSP Test Data](https://www.math.uwaterloo.ca/tsp/data/index.html):
- xqf131
- pbm436
- uy734
- rw1621

### Setting
100 iteration in meta-heuristic algorithm
## Future Work
To improved the algorithm we has two criterion:
### Idea improved
1. Meta-heuristic 
    - Using memetics algorithm to alternate the genetics algorithm
2. Heuristic(solution quality improved) 
    - Using 3-opt or **Lin-Kernighan** algorithm alternate the 2-opt algorithm but it will using more times
    
### Efficiency improved(time reduction but the result not change)
1. Using **cython** or **Jit** technique to speed-up python program
3. Using **splay tree** or other data structure to represent the tour([Data Structures for Traveling Salesmen](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.49.570&rep=rep1&type=pdf)) to speed up local search.
## Reference
[Traveling Salesman Problem   -wikipedia](https://en.wikipedia.org/wiki/Travelling_salesman_problem)
[Concorde TSP Solver   -wikipedia](https://en.wikipedia.org/wiki/Concorde_TSP_Solver)
[Concorde Home](https://www.math.uwaterloo.ca/tsp/concorde.html)
[Ant Colony Sytem](https://ieeexplore.ieee.org/abstract/document/585892)
[Genetic Algorithm for Traveling Salesman Problem with Modified Cycle Crossover Operator](https://www.hindawi.com/journals/cin/2017/7430125/)
[An Improved Genetic Algorithm for TSP](https://ieeexplore.ieee.org/abstract/document/4370274)
[Data Structures for Traveling Salesmen](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.49.570&rep=rep1&type=pdf)
