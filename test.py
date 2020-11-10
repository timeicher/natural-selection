import random

x = 37
y = 1000

initial_direction = 0



i_direction_range = 2

def initial_direction(x,y,initial_direction,i_direction_range):
    rand_range = random.randrange(0,i_direction_range+1) #General random range

    #Depending on the starting position the exact initial direction gets calculated.
    if x == 0:
        initial_direction = 0

    if x == 1000:
        pass

    if y == 0:
        pass

    if y == 1000:
        unclean_direction = 360 - (1/2) * i_direction_range + rand_range
    
    while unclean_direction > 360:
        unclean_direction -= 360

    initial_direction = unclean_direction

    return initial_direction

sol = initial_direction(x,y,initial_direction,i_direction_range)

print(sol)