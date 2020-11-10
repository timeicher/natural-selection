#################################################################################
   # Content : Main program of NATURAL SELECTION
   # Creator : Tim Eicher
   # Created : July 2020
   # Edited  : 15:43 10-11-2020
#################################################################################

#The different libraries are imported.
import pygame       #The world itself runs on pygame
import tkinter      #Graphical Interface for setting parameters
import random       #For chosing random numbers
import numpy as np  #For Vector Calculations
import math         #Functions for mathematical calculations (e.g sinus)

#Settings for the pygame implementation.
win_w = 1000
win_h = 1000

FPS = 60

run = True

#Settings for the simulation.
creature_size = 40
food_size = 10

num_of_creatures_beginning = 10
num_of_food_beginning = 20

food_border = 300 #define how far away from the border food spawns

i_direction_range = 90 #set the range in which creatures can go at the beginning.
standard_sense = 100 #How much a creature with a sense value of 1 is able to see (in pixels)


#The class for the creatures.
class creature:
    #Class Variables
    num_of_creatures = 0

    creatures_pos_x = []
    creatures_pos_y = []

    creatures_alive = []
    creatures_dead = []

    #Class functions
    def __init__(self):
        
        self.x = 0
        self.y = 0
        self.vector = np.array([self.x,self.y])
        self.initial_direction = 0

        self.alive = True
        self.energy = 1000

        self.velocity = 1
        self.sense = 1
        self.size = 1

        self.pathfinding = False

        creature.creatures_alive.append(self)
        creature.num_of_creatures += 1

    #A location for the first spawn gets searched
    def first_spawn(self,creature_size,creatures_pos_x,creatures_pos_y):
        decider = random.randrange(0,2)
        searching_active = True
        
        #The decider decides wheater creatures spawn across the x or y axis (0 = x-axis, 1 = y-axis).
        if decider == 0:
            
            while searching_active: #Searching active means, that a possible (unoccupied) location still hasn't been found.
                self.x = random.randrange(creature_size, (1000-2*creature_size)) #A random x position gets searched on the x axis, without the corners.
                self.y = random.choice([0, (1000-creature_size)]) #It gets selected randomly wheater the creature starts at the top or bottom.
                
                #It gets checked if there is another creature in the same place.
                counter1 = self.x
                for _ in range(creature_size):
                    if counter1 in creatures_pos_x:
                        searching_active = True
                        break

                    else:
                        searching_active = False
                        counter1 += 1

            #Every x from the new found creature gets saved.
            counter2 = self.x
            for _ in range(creature_size):
                creatures_pos_x.append(counter2)
                counter2 += 1

        if decider == 1:
            
            while searching_active:
                self.x = random.choice([0, (1000-creature_size)])
                self.y = random.randrange(creature_size,(1000-2*creature_size))
                counter1 = self.y
                
                for _ in range(creature_size):
                    if counter1 in creatures_pos_y:
                        searching_active = True
                        break

                    else:
                        searching_active = False
                        counter1 += 1

            counter2 = self.y
            for _ in range(creature_size):
                creatures_pos_y.append(counter2)
                counter2 += 1
        
        self.vector = np.array([self.x,self.y])

    #The function draws a creature on pygame.
    def draw(self,creature_size):
        pygame.draw.rect(win, (255,0,0), (int(self.x),int(self.y),creature_size,creature_size))
        pygame.draw.rect(win, (10,10,10), (int(self.x+5),int(self.y+5),creature_size-10,creature_size-10))

    #A random initial direction is given to all creatures.
    def direction(self,i_direction_range):
        rand_range = random.randrange(0,i_direction_range+1) #General random range

        #Depending on the starting position the exact initial direction gets calculated.
        if self.x == 0:
            self.initial_direction = 90 - (1/2) * i_direction_range + rand_range 

        elif self.x == 1000-creature_size:
            self.initial_direction = 270 - (1/2) * i_direction_range + rand_range

        elif self.y == 0:
            self.initial_direction = 180 - (1/2) * i_direction_range + rand_range

        elif self.y == 1000-creature_size:
            self.initial_direction = 360 - (1/2) * i_direction_range + rand_range

        #If the value is above 360 it subtracts 360.
        while self.initial_direction > 360:
            self.initial_direction -= 360


    #The function changes the x and y of a creature somewhat randomly.
    def move_searching(self,FPS):

        #For the x speed the cosinus is used. Because 0 degrees is pointing north I have to add 90 in order for it to function with the cosinus.
        self.x += self.velocity * math.cos(math.radians(self.initial_direction-90))


        #For the y speed the sinus is used. Because 0 degrees is pointing north I have to add 90 in order for it to function with the cosinus.
        self.y += self.velocity * math.sin(math.radians(self.initial_direction-90))


        #If the creature reaches the edge a new 
        #Depending on the position the exact initial direction gets calculated.
        if self.x <= 0:
            rand_range = random.randrange(0,i_direction_range+1) #General random range
            self.initial_direction = 90 - (1/2) * i_direction_range + rand_range

        elif self.x >= 1000-creature_size:
            rand_range = random.randrange(0,i_direction_range+1) #General random range
            self.initial_direction = 270 - (1/2) * i_direction_range + rand_range

        elif self.y <= 0:
            rand_range = random.randrange(0,i_direction_range+1) #General random range
            self.initial_direction = 180 - (1/2) * i_direction_range + rand_range

        elif self.y >= 1000-creature_size:
            rand_range = random.randrange(0,i_direction_range+1) #General random range
            self.initial_direction = 360 - (1/2) * i_direction_range + rand_range

        #If the value is above 360 it subtracts 360.
        while self.initial_direction > 360:
            self.initial_direction -= 360


    #If the creature has found food, this function pathfinds towards that food.
    def move_pathfinding(self):
        pass

    #This functions scans the surroundings of a creature for food. The higher the sense variable the better the sense.
    def scan(self,standard_sense):
        
        creature_boundries = [self.x+(1/2)*creature_size, self.y+(1/2)*creature_size]
        for creature_boundries in len(int(standard_sense*self.sense+1)):
            pass
        
            


    #The function checks if the creature can reproduce. If yes: the creature reproduces.
    def reproduce(self):
        pass


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
        food.food_not_eaten.append(self)

    #An unoccupied position for a food getssearched.
    def first_spawn(self,food_size,food_pos_x,food_pos_y):
        searching_active = True
            
        while searching_active: #Searching active means, that a possible (unoccupied) location still hasn't been found.
            self.x = random.randrange(food_border, (1000-food_border)) #A random x position, within the border, gets searched on the x axis.
            self.y = random.randrange(food_border, (1000-food_border)) #A random y position, within the border, gets searched on the y axis.
            
            #It gets checked if there is another food in the same place.
            counter1 = self.x
            counter2 = self.y
            for _ in range(food_size):
                if counter1 in food_pos_x and counter2 in food_pos_y:
                    searching_active = True
                    break

                else:
                    searching_active = False
                    counter1 += 1
                    counter2 += 1

        #Every x from the new found food gets saved.
        counter3 = self.x
        for _ in range(food_size):
            food_pos_x.append(counter3)
            counter3 += 1

        #Every y from the new found food gets saved.
        counter4 = self.y
        for _ in range(food_size):
            food_pos_y.append(counter4)
            counter4 += 1

    #The function draws one food on a predefined location.
    def draw(self, food_size):
        pygame.draw.rect(win, (0,0,255), (self.x,self.y,food_size,food_size))

    #The function removes the food from the grid.
    def get_eaten(self):
        pass
    

#################################################################################
  # Mainloop
#################################################################################

#New creatures and food instances get created.
for _ in range(num_of_creatures_beginning):
    creature_x = creature()

for _ in range(num_of_food_beginning):
    food_x = food()


#Pygame gets started.
pygame.init()
win = pygame.display.set_mode((win_w, win_h))

#The game gets named.
pygame.display.set_caption("Natural Selection")


#The first spawn gets done.
for self in creature.creatures_alive:
    self.first_spawn(creature_size,creature.creatures_pos_x,creature.creatures_pos_y)
    self.direction(i_direction_range)


for self in food.food_not_eaten:
    self.first_spawn(food_size,food.food_pos_x,food.food_pos_y)


#Loop
while run:
    #How often the screen gets drawn.
    pygame.time.delay(FPS)


    #The different elements get drawn and updated.
    win.fill ((240,240,240))
    
    
    #All creatures and food that are alive get drawn. Different functions get excecuted.
    for self in food.food_not_eaten:
        self.draw(food_size)


    for self in creature.creatures_alive:
        self.draw(creature_size)

        if self.pathfinding == False:
            self.move_searching(FPS)

    pygame.display.update()



    #If you press the close button the loop stops.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


#Debugging.



#Pygame gets closed.
pygame.quit()