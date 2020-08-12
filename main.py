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
    def first_spawn(self):
        pass

    #The function draws a creature on pygame.
    def draw(self):
        pass
    
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

#New creatures and food get spawned.
creature_1 = creature()

print(creature.creatures_alive, creature_1.energy)

#Pygame gets started.
pygame.init()
win = pygame.display.set_mode((win_w, win_h))

#The game gets named.
pygame.display.set_caption("Natural Selection")


while run:
    #How often the screen gets drawn.
    pygame.time.delay(FPS)


    #The different elements get drawn and updated.
    win.fill ((10,10,10))
    
    
    for i in creature.creatures_alive:
        pygame.draw.rect(win, (255,0,0), (50,50,5,5))


    pygame.display.update()



    #If you press the close button the loop stops.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

#Pygame gets closed.
pygame.quit()