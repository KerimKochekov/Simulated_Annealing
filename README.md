# Simulated Annealing

Simulated Annealing (SA) for Travelling Salesman Problem (TSP) for 30 most populated Russian cities.

# Problem Description

## TSP
Given a list of cities and the distances between each pair of cities, what is
the shortest possible route that visits each city once and returns to the origin
city? In our case cities were the 30 most populated Russian cities and distance was real geographical [**Haversine distance**](https://en.wikipedia.org/wiki/Haversine_formula)

## Approach
The energy distribution for this problem is easy to express in a format suitable for SA.

  $p^∗_sales(path) = e ^{− dist(path)/T}$
  
where *path* is the ordered list of cities to visit, dist is the function that computes path distance. The main trick to solve traveling salesman with SA is to pick a proper proposal distribution. The common proposal policy for this problem is the following:
1. Pick two cities in the path;
2. Exchange their positions in the path;
3. Return to the new proposed path.
- ``algorithm/SA_algorithm.py``: You can find my implemented SA algorithm for TSP here.

# Algorithm
1. Sample initial $x_0$, set time step t = 0;
2. Set initial temperature T. To avoid problems with numerical overflow when calculating the exponent, set the temperature compared with the initial value of the system’s energy;
3. Generate $x′$ from $g(x′|x_t)$. For continuous problems, the common solution is to use the normal distribution;
4. Calculate acceptance ratio $α = \frac{p∗(x')}{p∗(x_t)}$;
5. Generate $u ∼ U(0,1)$. If $u ≤ α$, accept the new state $x_{t+1} = x′$, otherwise propagate the old state. Pass x_{t+1} to the output of the sampler;
6. Reduce temperature T. Temperature annealing does not have to occur on every iteration. The temperature can be decreased every N iteration as well. There is no strict rule about this;
7. Increment t;
8. Repeat 2-8 until cooled down. The solution can be sampled before the system is cooled down, but we don't know whether this was the optimal solution.

# Data
- https://github.com/hflabs/city

## Data preprocessing
- ``algorithm/processing.py``: Since provided dataset contains too many unneeded details in columns, we need to apply some preprocessing (dropping some columns) and sorting (by population) to get this table. You can find the table file here [top-30](https://github.com/KerimKochekov/Simulated_Annealing/blob/main/algorithm/top-30_cities.csv).

| address         | geo_lat    | geo_lon     |
|-----------------|------------|-------------|
| Москва          | 55.7540471 | 37.620405   |
| Санкт-Петербург | 59.9391313 | 30.3159004  |
| Новосибирск     | 55.028191  | 82.9211489  |
| Екатеринбург    | 56.8385216 | 60.6054911  |
| Нижний Новгород | 56.3240627 | 44.0053913  |
| Казань          | 55.7943584 | 49.1114975  |
| Самара          | 53.1950306 | 50.1069518  |
| Омск            | 54.9848566 | 73.3674517  |
| Челябинск       | 55.1602624 | 61.4008078  |
| Ростов-на-Дону  | 47.2224566 | 39.718803   |
| Уфа             | 54.734944  | 55.9578468  |
| Волгоград       | 48.7070042 | 44.5170339  |
| Пермь           | 58.0102583 | 56.2342034  |
| Красноярск      | 56.0093879 | 92.8524806  |
| Воронеж         | 51.6593332 | 39.1969229  |
| Саратов         | 51.533557  | 46.034257   |
| Краснодар       | 45.0401604 | 38.9759647  |
| Тольятти        | 53.5205348 | 49.3894028  |
| Барнаул         | 53.3479968 | 83.7798064  |
| Ижевск          | 56.852738  | 53.2114896  |
| Ульяновск       | 54.3079415 | 48.3748487  |
| Владивосток     | 43.1164904 | 131.8823937 |
| Ярославль       | 57.6215477 | 39.8977411  |
| Иркутск         | 52.2864036 | 104.2807466 |
| Тюмень          | 57.1529744 | 65.5344099  |
| Махачкала       | 42.9849159 | 47.5047181  |
| Хабаровск       | 48.4647258 | 135.0598942 |
| Оренбург        | 51.7875092 | 55.1018828  |
| Новокузнецк     | 53.794315  | 87.2142745  |
| Кемерово        | 55.3910651 | 86.0467781  |

# Results
We can consider an answer in the range of [17k, 20k] is sufficient. But I wanted to know the global minimum (best possible) for this specific problem (for given 30 cities). Due to that other than the SA algorithm, I implemented a heuristic solution that uses **Dynamic programming+Bitmask** with $O(2^n*n)$ execution time (~80 minutes of running for n = 30) and found the best possible answer (global minimum) as 17908. 

Laterward ran the SA algorithm with slow cooling and fast cooling, luckily both approaches after some iterations (slow in 30-40 iterations and fast in 10-15 iterations) found 17908 as a minimum answer in less than one minute. As result, the SA algorithm can be poor for some combinatorial problems, but here for TSP, it worked perfectly in less time for different hyperparameters of temperature.
[![Slow cooling](https://github.com/KerimKochekov/Simulated_Annealing/blob/main/bin/final.png)](https://youtu.be/3JeDslGMP-k)

## Cooling hyperparamteres
- Initial temperature: 100
- Final temperature: 20
- Number of iterations per decay: 10.000

## Slow cooling
- Temperature decay: 0.99
![](https://github.com/KerimKochekov/Simulated_Annealing/blob/main/bin/slow_cooling.png)

## Middle cooling
- Temperature decay: 0.95
![](https://github.com/KerimKochekov/Simulated_Annealing/blob/main/bin/middle_cooling.png)

## Fast cooling
- Temperature decay: 0.9
![](https://github.com/KerimKochekov/Simulated_Annealing/blob/main/bin/fast_cooling.png)

## Final answer (~17.908km) on real Map
- Used https://www.daftlogic.com/projects-google-maps-distance-calculator.htm
![](https://github.com/KerimKochekov/Simulated_Annealing/blob/main/bin/terminal.png)
