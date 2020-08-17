import random

creatures_pos_x = [2,3,4]
creatures_pos_y = []
creature_size = 2

def first_spawn(creature_size,creatures_pos_x,creatures_pos_y):
        decider = 0  #random.randrange(0,2)
        searching_active = True
        
        #The decider decides wheater creatures spawn across the x or y axis (0 = x-axis, 1 = y-axis).
        if decider == 0:
            
            while searching_active: #Searching active means, that a possible (unoccupied) location still hasn't been found.
                x = random.randrange(creature_size, (10-2*creature_size)) #A random x position gets searched on the x axis, without the corners.
                y = random.choice([0, (10-creature_size)]) #It gets selected randomly wheater the creature starts at the top or bottom.
                if x in creatures_pos_x:
                    pass
                else:
                    searching_active = False
                
                    #Every x from the new found creature gets saved.
                    counter = x
                    for _ in range(creature_size+1):
                        creatures_pos_x.append(counter)
                        counter += 1
                

        if decider == 1:
            
            while searching_active:
                self.x = random.choice([0, (10-creature_size)])
                self.y = random.randrange(creature_size,(10-2*creature_size))
                if self.y in creatures_pos_y:
                    pass
                else:
                    searching_active = False

                    counter = self.y
                    for _ in range(creature_size+1):
                        creatures_pos_y.append(counter)
                        counter += 1
        
        return x,y

x = first_spawn(creature_size,creatures_pos_x,creatures_pos_y)
print(x)
