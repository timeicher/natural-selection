import numpy as np
import math



velocity = 1

vector = np.array([100,300])

vector_long = np.array([500,500]) - vector #The vector from the creature to the middle of the field with the wrong length gets calculated.


velocity_x = vector_long[0]
velocity_y = vector_long[1]

#Formel für Vektorverkürzung für die richtige länge nach geschwindigkeit
t = math.sqrt((velocity_x**2 + velocity_y**2) / velocity**2)

vector_right = np.array([vector_long[0]/t,vector_long[1]/t])

velocity_x = vector_right[0]
velocity_y = vector_right[1]

print(velocity_x,velocity_y,vector_right)