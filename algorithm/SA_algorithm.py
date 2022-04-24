import math
import pandas as pd
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

def haversine_distance(A, B): 
    R = 6371.0710; # Radius of the Earth in kilometers
    rlat1 = A[0] * (math.pi/180); # Convert degrees to radians
    rlat2 = B[0] * (math.pi/180); # Convert degrees to radians
    difflat = rlat2 - rlat1 # Radian difference (latitudes)
    difflon = (B[1]-A[1]) * (math.pi/180) # Radian difference (longitudes)

    d = 2 * R * math.asin(math.sqrt(math.sin(difflat/2)*math.sin(difflat/2)+
        math.cos(rlat1)*math.cos(rlat2)*math.sin(difflon/2)*math.sin(difflon/2)))
    return d

def show(coordinates): #print the coordinates
    for i in range(-1, 30, 1):
        print(str(coordinates[i][0])+","+str(coordinates[i][1]))

def travel_cost(coordinates): #compute energy, or in other word cost of TSP
    cost = 0.0
    for i in range(-1, 29, 1):
        cost += haversine_distance(coordinates[i], coordinates[i+1])
    return cost

cities = pd.read_csv('top-30_cities.csv')
coordinates = list(zip(cities['geo_lat'], cities['geo_lon']))
x = [coor[1] for coor in coordinates]
y = [coor[0] for coor in coordinates]

#animiation initalization
fig, ax = plt.subplots(figsize=(16, 9))
ax.scatter(x, y)
for i, city in enumerate(cities["address"]):
    ax.annotate(city, xy = (x[i], y[i]))

line, = ax.plot([], [])
temperature_text = ax.text(0.85, 0.95, s='', fontsize=12, transform = ax.transAxes, bbox=dict(facecolor='green', alpha=0.3))
energy_text = ax.text(0.85, 0.90, s='', fontsize=12, transform = ax.transAxes, bbox=dict(facecolor='green', alpha=0.3))

#start of algorithm
current_cost = travel_cost(coordinates)

T = 100
T_final = 40
factor = 0.99 #slow cooling
#factor = 0.95 #middle cooling
#factor = 0.9 #fast cooling

best_cost = current_cost
best_coors = coordinates

states = []
temps = []

while T > T_final:
    if current_cost < best_cost:
        best_cost = current_cost
        best_coors = coordinates
        #show(best_coors)
         
    T *= factor
    for __ in range(10000):
        i, j = np.random.randint(0, 30, size = 2)
        #swap
        coordinate = coordinates[i]
        coordinates[i] = coordinates[j]
        coordinates[j] = coordinate

        new_cost = travel_cost(coordinates)

        if new_cost < current_cost:
            current_cost = new_cost
        else:
            prob = np.random.uniform()
            if prob < np.exp((current_cost-new_cost)/T):
                current_cost = new_cost
            else:
                coordinate = coordinates[i]
                coordinates[i] = coordinates[j]
                coordinates[j] = coordinate

    states.append(coordinates.copy())
    temps.append(T)


#print(best_cost)

def init():
    line.set_data([], [])
    energy_text.set_text('')
    temperature_text.set_text('')
    return line, temperature_text, energy_text

def animate(i):
    x = [state[1] for state in states[i]]
    #x.append(states[0][1])
    y = [state[0] for state in states[i]]
    #y.append(states[0][0])
    energy_text.set_text('Energy: {}'.format(int(travel_cost(states[i]))))
    temperature_text.set_text("Temperature: {}".format(int(temps[i])))
    line.set_data(x, y)
    return line

anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=len(states), interval=100, blit=False)

anim.save('animation.mp4', fps=1)