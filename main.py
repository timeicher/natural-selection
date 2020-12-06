#################################################################################
   # Content : Main program of NATURAL SELECTION
   # Creator : Tim Eicher
   # Created : July 2020
   # Edited  : 17:44 06-12-2020
#################################################################################

#The different libraries are imported.
import pygame               #The world itself runs on pygame
import tkinter              #Graphical Interface for setting parameters
import random               #For chosing random numbers
import numpy as np          #For Vector Calculations
import math                 #Functions for mathematical calculations (e.g sinus)
from copy import deepcopy   #A function for creating a clean copy from a class list.
import pandas as pd         #Creating and saving excel files easily for storing the data collected in the simulation.


#Settings for the pygame implementation.
win_w = 1000
win_h = 1000

FPS = 0 #FPS is wrong its the simulation speed. The lower the number the faster the simulation.

run = True

#Keeps track of the rounds that will still be played
roundcounter = 0

#Variables for the rounds.
simluating = True

#Settings for the simulation.
creature_size = 40
food_size = 10

num_of_creatures_beginning = 5
num_of_food_beginning = 20

food_border = 300 #define how far away from the border food spawns
radius = 500 - creature_size #The boundry for the food (or the island).
radius_food = 200 - (1/2) * food_size

reproducing_energy = 2000 #How much energy does a creature require to reproduce.
reproducing_cost = 1000 #How much does it cost to reproduce.
mutation_range = 1 #How much can a descendant differ from its parent. (In decimals e.g. 1 => +-0.1)

i_direction_range = 90 #set the range in which creatures can go at the beginning.
standard_sense = 100 #How much a creature with a sense value of 1 is able to see (in pixels)
eat_range = 5 #How many pixels does a creature need to come close to a food to eat it.

turn_constant = 1 #The change of the vector gets multiplied with the turn_constant for the calculation of the turn energy use.
search_constant = 2 #The energy substracted by sensing its environment gets multipliedf with the search_constant for the calculation of the energy use.
move_constant = 1 #The energy substracted by moving (e.g. air resistance) gets multiplied with the search_constant for the calculation of the energy use.

#Statistics.
change_speed = []
change_sense = []
change_num_of_creatures = []

#The class for the creatures.
class creature:
    #Class Variables
    num_of_creatures = 0

    #The positions of the creatures.
    creatures_pos_x = []
    creatures_pos_y = []

    #All creatures (dead and alive ones) in separate lists.
    creatures_alive = []
    creatures_dead = []

    #Food which is currently being eaten.
    food_being_eaten = []

    #Class functions
    def __init__(self):
        
        #Coordinates
        self.x = 0
        self.y = 0
        self.vector = np.array([self.x,self.y])
        self.initial_direction = 0

        #The x and y speed.
        self.velocity_x = 0
        self.velocity_y = 0

        #Vital signs of the creature.
        self.alive = True
        self.awake = True
        self.energy = 1000

        #Genes
        self.velocity = 1
        self.sense = 1
        self.size = 1

        #Dirfferent modes and variables of the creature.
        self.pathfinding = False
        self.found_food = "none" #If the creature senses a food nearby the information gets saved in this variable.

        #The creature gets appended to the alive creatures list.
        creature.creatures_alive.append(self)
        creature.num_of_creatures += 1

    #A location for the first spawn gets searched
    def first_spawn(self,creature_size,creatures_pos_x,creatures_pos_y,radius):

        #A random angle between 0, 360 degrees for the new spawn gets selected.
        starting_angle = random.randrange(0,361)
        
        self.x = 500 - (1/2) * creature_size + radius * math.cos(math.radians(starting_angle-90))
        self.y = 500 - (1/2) * creature_size + radius * math.sin(math.radians(starting_angle-90))

        self.vector = np.array([self.x,self.y])

    #The function draws a creature on pygame.
    def draw(self,creature_size):
        pygame.draw.rect(win, (255,0,0), (int(self.x),int(self.y),creature_size,creature_size))
        pygame.draw.rect(win, (10,10,10), (int(self.x+5),int(self.y+5),creature_size-10,creature_size-10))

    #The initial direction is calculated for a creature.
    def direction(self,creature_size):
        
        #The vector from the creature to the middle of the world gets calculated. It hasn't the right length yet.
        vector_long = np.array([500-(1/2)*creature_size,500-(1/2)*creature_size]) - np.array([self.x+(1/2)*creature_size,self.y+(1/2)*creature_size])
        
        #The formula for getting the divisor for the right length respective to the velocity of the creature.
        t = math.sqrt((vector_long[0]**2 + vector_long[1]**2) / self.velocity**2)
        
        #The vector with the right length gets calculated with the divisor t.
        vector_right = np.array([vector_long[0]/t,vector_long[1]/t]) 
        

        #The change in velocity gets calculated for the energy consumption.
        delta_vector_x = self.velocity_x - vector_right[0]
        delta_vector_y = self.velocity_y - vector_right[1]
        delta_vector_squared = (delta_vector_x ** 2 + delta_vector_y ** 2)

        self.energy -= delta_vector_squared * turn_constant

        #The vector gets split up in the 2 velocities.
        self.velocity_x = vector_right[0]
        self.velocity_y = vector_right[1]

    #The function changes the x and y of a creature somewhat randomly.
    def move_searching(self,FPS,creature_size,move_constant):

        #The x component gets added.
        self.x += self.velocity_x

        #The y component gets added.
        self.y += self.velocity_y

        #The vector gets updated
        self.vector = np.array([self.x,self.y])
        
        #If the creature reaches the edge the direction updates to the middle of the field again.
        if self.x <= 0 or self.x >= 1000-creature_size or self.y <= 0 or self.y >= 1000-creature_size:
            creature.direction(self,creature_size)

        #The energy for the velcity gets substracted.
        self.energy -= (self.velocity ** 2) * move_constant
       
    #If the creature has found food, this function pathfinds towards that food.
    def move_pathfinding(self,creature_size,food_size,move_constant):
        
        #The vector for pathfinding to the food gets calculated.(For further information see: creature.direction())
        vector_long = np.array([self.found_food.x+(1/2)*food_size,self.found_food.y+(1/2)*food_size]) - np.array([self.x+(1/2)*creature_size,self.y+(1/2)*creature_size])
        t = math.sqrt((vector_long[0]**2 + vector_long[1]**2) / self.velocity**2)

        vector_right = np.array([vector_long[0]/t,vector_long[1]/t]) 


        #The change in velocity gets calculated for the energy consumption.
        delta_vector_x = self.velocity_x - vector_right[0]
        delta_vector_y = self.velocity_y - vector_right[1]
        delta_vector_squared = (delta_vector_x ** 2 + delta_vector_y ** 2)

        self.energy -= delta_vector_squared * turn_constant

        self.velocity_x = vector_right[0]
        self.velocity_y = vector_right[1]

        #The x component gets added.
        self.x += self.velocity_x


        #The y component gets added.
        self.y += self.velocity_y

        #The vector gets updated
        self.vector = np.array([self.x,self.y])

        #The energy for the velcity gets substracted.
        self.energy -= (self.velocity ** 2) * move_constant

    #The function checks if the creature has reached the boundry of the world (the circle) again.
    def check_boundry(self,creature_size):
        
        #The vector between the creature and the food gets calculated (pos food - pos creature)
        vector_cb = np.array([500 - (self.x + (1/2) * creature_size), 500 - (self.y + (1/2) * creature_size)])
        
        #The distance of the new vector gets calculated.
        distance_cb = math.sqrt(vector_cb[0]**2+vector_cb[1]**2)

        if distance_cb >= radius:
            self.awake = False

    #This functions scans the surroundings of a creature for food. The higher the sense variable the better the sense.
    def scan(self,standard_sense,creature_size,food_size,food_pos_x,food_pos_y,search_constant):
        
        #The radius in which the creature checks for food. (In a circle around it)
        scan_radius = standard_sense * self.sense

        food_found = False

        list_distance = []

        #The energy used for scanning gets substracted.
        self.energy -= (self.sense ** 2) * search_constant

        #All food gets checked whether it is close enough to be seen by the creature.
        for scanned_food in food.food_not_eaten:
            
            #The vector between the creature and the food gets calculated (pos food - pos creature)
            vector_cf = np.array([(scanned_food.vector[0] + (1/2) * food_size) - (self.vector[0] + (1/2) * creature_size), (scanned_food.vector[1] + (1/2) * food_size) - (self.vector[1] + (1/2) * creature_size)])
            
            #The distance of the new vector gets calculated.
            distance_cf = math.sqrt(vector_cf[0]**2+vector_cf[1]**2)

            #The value gets appended to the list with all distances.
            list_distance.append(distance_cf)

        
        #The smallest distance gets identified and then associated with the food.
        if list_distance != []:    
            smallest = min(list_distance)
        
            smallest_food_pos = list_distance.index(smallest)
            
            smallest_food = food.food_not_eaten[smallest_food_pos]

            #The vector between the creature and the closest food gets calculated.
            vector_cf = np.array([(smallest_food.vector[0] + (1/2) * food_size) - (self.vector[0] + (1/2) * creature_size), (smallest_food.vector[1] + (1/2) * food_size) - (self.vector[1] + (1/2) * creature_size)])
            
            distance_cf = math.sqrt(vector_cf[0]**2+vector_cf[1]**2)


            #Is the food in the scan_radius of the creature?
            if distance_cf <= scan_radius:
        
                food_found = True


        #The creature now goes into the mode where it pathfinds to the food; The last scanned food gets returned if it was inside the radius.
        if food_found == True:
            if not smallest_food in creature.food_being_eaten:
                self.pathfinding = True
                self.found_food = smallest_food

                creature.food_being_eaten.append(smallest_food) #The food gets appended to the list of food which is currently being eaten.


        #If no food has been found the word none gets returned. 
        else:
            return "none"
        
    #The function checks if the creature can reproduce. If yes, the creature reproduces.
    def reproduce(self,mutation_range):
        
        if self.energy >= reproducing_energy:

            self.create_newborn(mutation_range)

    #Create a new creature instance based on its parent.
    def create_newborn(self,mutation_range):

        #New creature instance.
        new_creature = creature()

        #The velocity and sense values of the new creature are the same as those of the parent with a chance of mutation. (mutation_range)
        new_creature.velocity = (self.velocity - (mutation_range/10) + (random.randrange(0,2*mutation_range+1)/10))

        new_creature.sense = (self.sense - (mutation_range/10) + (random.randrange(0,2*mutation_range+1)/10))

    #The creature eats the food which is close to it.
    def eat(self,eat_range):
        
        #The vector between the creature and the food gets calculated (pos food - pos creature)
        vector_cf = np.array([(self.found_food.vector[0] + (1/2) * food_size) - (self.vector[0] + (1/2) * creature_size), (self.found_food.vector[1] + (1/2) * food_size) - (self.vector[1] + (1/2) * creature_size)])
        
        #The distance of the new vector gets calculated.
        distance_cf = math.sqrt(vector_cf[0]**2+vector_cf[1]**2)

        #If the food is close enough it gets eaten.
        if distance_cf <= eat_range:
            self.energy += self.found_food.energy
            self.found_food.get_eaten()
            self.pathfinding = False

    #It gets checked if the creature is still alive.
    def check_alive(self):

        if self.energy <= 0:

            self.alive == False

            creature.creatures_dead.append(self)
            creature.creatures_alive.remove(self)

            return True



#The class for the food.
class food:

    food_not_eaten = []
    food_eaten = []

    food_pos_x = []
    food_pos_y = []    

    def __init__(self):
        self.energy = 500
        self.eaten = False
        
        self.x = 0
        self.y = 0
        self.vector = np.array([self.x,self.y])

        food.food_not_eaten.append(self)

    #An unoccupied position for a food getssearched.
    def first_spawn(self,food_size,food_pos_x,food_pos_y,radius_food):
        #A random angle between 0, 360 degrees for the new spawn gets selected.
        starting_angle = random.randrange(0,361)

        radius = random.randrange(0,radius_food+1)
        
        self.x = 500 - (1/2) * food_size + radius * math.cos(math.radians(starting_angle-90))
        self.y = 500 - (1/2) * food_size + radius * math.sin(math.radians(starting_angle-90))

        self.vector = np.array([self.x,self.y])

    #The function draws one food on a predefined location.
    def draw(self, food_size):
        pygame.draw.rect(win, (0,0,255), (self.x,self.y,food_size,food_size))

    #The function removes the food from the grid.
    def get_eaten(self):
        food.food_eaten.append(self)
        
        if self in food.food_not_eaten:
            food.food_not_eaten.remove(self)


#The global lists so other classes can work with it.
food_pos_x = []
food_pos_y = []

#A list for the reproducing gets created.
parent_gen = []

#################################################################################
  # Mainloop
#################################################################################

#How should the file be called where the collected data will be stored.
filename = input("How should the file be called where the data will be saved?") + ".xlsx"


#New creatures and food instances get created.
for _ in range(num_of_creatures_beginning):
    creature_x = creature()


#Pygame gets started.
pygame.init()
win = pygame.display.set_mode((win_w, win_h))

#The game gets named.
pygame.display.set_caption("Natural Selection")


#The class food values become normal values so they are usable for other classes.
food.food_pos_x = food_pos_x
food.food_pos_y = food_pos_y

#Every round is one loop through here.
while True:


    if roundcounter == 0:
        #How many rounds are simulated.
        decision = int(input("How many days do you want to simulate?(number for amount of rounds / 0=exit)" + "\n"))

        if decision == 0:
            break

        elif decision > 0:
            roundcounter = decision

    roundcounter -= 1

    #Printing
    for self in creature.creatures_alive:
        print(self.velocity,self.sense)
        print("\n")

    breaking = False
    over = False

    #The new creatures get spawned and get a direction.
    for self in creature.creatures_alive:
        self.first_spawn(creature_size,creature.creatures_pos_x,creature.creatures_pos_y,radius)
        self.direction(creature_size)
        
        #Variables get reset
        self.awake = True

    #The speed of the current generation gets saved in a new list.
    current_generation = []

    for self in creature.creatures_alive:
        current_generation.append(self.velocity)

    #...and appended to the list containing the speed of every generation.
    change_speed.append(current_generation)

    
    
    #The sense of the current generation gets saved in a new list.
    current_generation = []

    for self in creature.creatures_alive:
        current_generation.append(self.sense)

    #...and appended to the list containing the sense of every generation.
    change_sense.append(current_generation)


    #The num of creatures of the current round get saved.
    creature_counter = 0

    for self in creature.creatures_alive:
        creature_counter += 1

    change_num_of_creatures.append(creature_counter)




    #The new food generation gets spawned.
    food.food_not_eaten = []
    food.food_eaten = []
    
    for _ in range(num_of_food_beginning):
        food_x = food()

    for self in food.food_not_eaten:
        self.first_spawn(food_size,food.food_pos_x,food.food_pos_y,radius_food)

    #Looploop
    while over == False:
        #How much the simulation gets slowed down.
        pygame.time.delay(FPS)


        #The screen gets filled with white.
        win.fill ((10,10,10))
        pygame.draw.circle(win,(240,240,240),(500,500),500)
        
        #Food which has not been eaten gets drawn.
        for self in food.food_not_eaten:
            self.draw(food_size)

        #All creatures get checked if they are still alive.
        for self in creature.creatures_alive:
            self.check_alive()

        #Alive creatures execute functions.
        for self in creature.creatures_alive:
            
            self.draw(creature_size)
            
            
            if self.awake == True:
                if self.pathfinding == False:
                    self.move_searching(FPS,creature_size,move_constant)
                    self.scan(standard_sense,creature_size,food_size,food_pos_x,food_pos_y,search_constant)
                
                elif self.pathfinding == True:
                    self.move_pathfinding(creature_size,food_size,move_constant)
                    self.eat(eat_range)
            
            self.check_boundry(creature_size)

            
        pygame.display.update()


        #If all creatures aren't awake anymore the round is over.
        for self in creature.creatures_alive:
            
            over = False
            if self.awake == True:
                over = False
                break
            
            elif self.awake == False:
                over = True
        
        #Does the user want to close the window?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                over = True
                breaking = True
        
        #Are all creatures dead?
        if creature.creatures_alive == []:
            break


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            over = True
            break

    if breaking == True:
        break


    #Reproducing
    #Deepcopy makes it a completely new list.
    parent_gen = deepcopy(creature.creatures_alive)

    #Reproducing.
    for self in parent_gen:
        self.reproduce(mutation_range)
    

#Saving to excel.
data_speed = pd.DataFrame({"Speed": change_speed})
data_sense = pd.DataFrame({"Sense": change_sense})
data_num = pd.DataFrame({"Number of creatures": change_num_of_creatures})

datatoexcel = pd.ExcelWriter(filename,engine="xlsxwriter")

data_speed.to_excel(datatoexcel, sheet_name="speed")
data_sense.to_excel(datatoexcel, sheet_name="sense")
data_num.to_excel(datatoexcel, sheet_name="number of creatures")

datatoexcel.save()


#Debugging.



#Pygame gets closed.
pygame.quit()