#################################################################################
   # Content : Main program of NATURAL SELECTION
   # Creator : Tim Eicher
   # Created : July 2020
   # Edited  : 13:30 11-08-2020
#################################################################################

#The different libraries are imported.
import pygame
import tkinter
import random

#Settings for the pygame implementation.
win_w = 1000
win_h = 1000

FPS = 60

run = True

#Settings for the simulation.
creature_size = 50
food_size = 50

num_of_creatures_beginning = 3




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
                counter1 = self.x
                
                for _ in range(creature_size):
                    if counter1 in creatures_pos_x:
                        searching_active = True
                        break

                    else:
                        searching_active = False
                        counter1 += 1

                    counter2 = self.y
                    for _ in range(creature_size):
                        creatures_pos_y.append(counter2)
                        counter2 += 1

    #The function draws a creature on pygame.
    def draw(self,creature_size):
        pygame.draw.rect(win, (255,0,0), (self.x,self.y,creature_size,creature_size))
    
    #The function changes the x and y of a creature somewhat randomly.
    def move_searching(self):
        pass
    
    #This functions scans the surroundings of a creature for food. The higher the sense variable the better the sense.
    def scan(self):
        pass

    #If the creature has found food, this function pathfinds towards that food.
    def move_pathfinding(self):
        pass

    #The function checks if the creature can reproduce. If yes: the creature reproduces.
    def reproduce(self):
        pass


#The class for the food.
class food:

    def __init__(self):
        self.energy = 500
        self.eaten = False
    
    #The function draws one food on a predefined location.
    def draw(self):
        pass

    #The function removes the food from the grid.
    def get_eaten(self):
        pass
    

#################################################################################
  # Mainloop
#################################################################################

#New creatures and food instances get created.
creature_1 = creature()
creature_2 = creature()
creature_3 = creature()
creature_4 = creature()
creature_5 = creature()
creature_6 = creature()



#Pygame gets started.
pygame.init()
win = pygame.display.set_mode((win_w, win_h))

#The game gets named.
pygame.display.set_caption("Natural Selection")


#The first spawn gets done.
for self in creature.creatures_alive:
    self.first_spawn(creature_size,creature.creatures_pos_x,creature.creatures_pos_y)

#Loop
while run:
    #How often the screen gets drawn.
    pygame.time.delay(FPS)


    #The different elements get drawn and updated.
    win.fill ((10,10,10))
    
    
    #All creatures that are alive get spawned.
    for self in creature.creatures_alive:
        self.draw(creature_size)
        

    pygame.display.update()



    #If you press the close button the loop stops.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


#Debugging.


#Pygame gets closed.
pygame.quit()