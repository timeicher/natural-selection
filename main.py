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

FPS = 30

run = True

#Settings for the simulation.
creature_size = 40
food_size = 10

num_of_creatures_beginning = 10
num_of_food_beginning = 20

food_border = 300 #define how far away from the border food spawns

i_direction_range = 90 #set the range in which creatures can go at the beginning.
standard_sense = 100 #How much a creature with a sense value of 1 is able to see (in pixels)
eat_range = 5 #How many pixels does a creature need to come close to a food to eat it.

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

    #The initial direction is calculated for a creature.
    def direction(self,creature_size):
        
        #The vector from the creature to the middle of the world gets calculated. It hasn't the right length yet.
        vector_long = np.array([500-(1/2)*creature_size,500-(1/2)*creature_size]) - np.array([self.x+(1/2)*creature_size,self.y+(1/2)*creature_size])
        

        #The formula for getting the divisor for the right length respective to the velocity of the creature.
        t = math.sqrt((vector_long[0]**2 + vector_long[1]**2) / self.velocity**2)
        
        #The vector with the right length gets calculated with the divisor t.
        vector_right = np.array([vector_long[0]/t,vector_long[1]/t]) 
        
        #The vector gets split up in the 2 velocities.
        self.velocity_x = vector_right[0]
        self.velocity_y = vector_right[1]


    #The function changes the x and y of a creature somewhat randomly.
    def move_searching(self,FPS,creature_size):

        #The x component gets added.
        self.x += self.velocity * self.velocity_x


        #The y component gets added.
        self.y += self.velocity * self.velocity_y

        #The vector gets updated
        self.vector = np.array([self.x,self.y])
        
        #If the creature reaches the edge the direction updates to the middle of the field again.
        if self.x <= 0 or self.x >= 1000-creature_size or self.y <= 0 or self.y >= 1000-creature_size:
            creature.direction(self,creature_size)
       


    #If the creature has found food, this function pathfinds towards that food.
    def move_pathfinding(self,creature_size,food_size):
        
        #The vector for pathfinding to the food gets calculated.(For further information see: creature.direction())
        vector_long = np.array([self.found_food.x+(1/2)*food_size,self.found_food.y+(1/2)*food_size]) - np.array([self.x+(1/2)*creature_size,self.y+(1/2)*creature_size])
        t = math.sqrt((vector_long[0]**2 + vector_long[1]**2) / self.velocity**2)

        vector_right = np.array([vector_long[0]/t,vector_long[1]/t]) 

        self.velocity_x = vector_right[0]
        self.velocity_y = vector_right[1]

        #The x component gets added.
        self.x += self.velocity * self.velocity_x


        #The y component gets added.
        self.y += self.velocity * self.velocity_y

        #The vector gets updated
        self.vector = np.array([self.x,self.y])


    #This functions scans the surroundings of a creature for food. The higher the sense variable the better the sense.
    def scan(self,standard_sense,creature_size,food_size,food_pos_x,food_pos_y):
        
        #The radius in which the creature checks for food. (In a circle around it)
        scan_radius = standard_sense*self.sense

        food_found = False

        #All food gets checked whether it is close enough to be seen by the creature.
        for scanned_food in food.food_not_eaten:
            
            #The vector between the creature and the food gets calculated (pos food - pos creature)
            vector_cf = np.array([(scanned_food.vector[0] + (1/2) * food_size) - (self.vector[0] + (1/2) * creature_size), (scanned_food.vector[1] + (1/2) * food_size) - (self.vector[1] + (1/2) * creature_size)])
            
            #The distance of the new vector gets calculated.
            distance_cf = math.sqrt(vector_cf[0]**2+vector_cf[1]**2)

            if distance_cf <= scan_radius:

                food_found = True
                break

        #The creature now goes into the mode where it pathfinds to the food; The last scanned food gets returned if it was inside the radius.
        if food_found == True:
            if not scanned_food in creature.food_being_eaten:
                self.pathfinding = True
                self.found_food = scanned_food

                creature.food_being_eaten.append(scanned_food) #The food gets appended to the list of food which is currently being eaten.


        #If no food has been found the word none gets returned. 
        else:
            return "none"


    #The function checks if the creature can reproduce. If yes, the creature reproduces.
    def reproduce(self):
        pass

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
            print("did it work?")




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
        
        self.vector = np.array([self.x,self.y])

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
        food.food_eaten.append(self)
        food.food_not_eaten.remove(self)


#The global lists so other classes can work with it.
food_pos_x = []
food_pos_y = []


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
    self.direction(creature_size)


for self in food.food_not_eaten:
    self.first_spawn(food_size,food.food_pos_x,food.food_pos_y)


#The class food values become normal values so they are usable for other classes.
food.food_pos_x = food_pos_x
food.food_pos_y = food_pos_y

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
            self.move_searching(FPS,creature_size)
            self.scan(standard_sense,creature_size,food_size,food_pos_x,food_pos_y)
        
        elif self.pathfinding == True:
            self.move_pathfinding(creature_size,food_size)
            self.eat(eat_range)
        
        


    pygame.display.update()



    #If you press the close button the loop stops.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


#Debugging.



#Pygame gets closed.
pygame.quit()