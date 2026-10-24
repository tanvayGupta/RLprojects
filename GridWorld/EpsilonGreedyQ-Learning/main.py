import numpy as np

ALPHA = 0.1
GAMMA = 0.8

class GridWorld():
    def __init__(self, size=5, pits = [[1,3],[2,1]], goal=None):
        self.size = size
        self.pos = [0,0]
        self.next_pos = [0,0]
        self.step_reward = -1
        self.pit_reward = -10
        self.goal_reward = 20

        self.goal_counter = 0


        self.goal = [size-1,size-1]
        self.pits = pits
        self.reset()
        self.av = np.zeros((size,size,4))

        

    def reset(self):
        self.pos = (0,0)
        return self.pos

    def trial_left(self):
       self.next_pos = [self.pos[0],max(0,self.pos[1]-1)]
       self.av[self.pos[0],self.pos[1]] += ALPHA *  (self.step_reward + (GAMMA * self.av[(self.next_pos[0],self.next_pos[1])].max()))

       self.pos = self.next_pos
       print(self.av[self.pos[0],self.pos[1],0])
       print(self.next_pos)

    def trial_right(self):
           self.next_pos = [self.pos[0],min(self.size-1,self.pos[1]+1)]
           self.av[self.pos[0],self.pos[1]] += ALPHA *  (self.step_reward + (GAMMA * self.av[(self.next_pos[0],self.next_pos[1])].max()))
    
           self.pos = self.next_pos
           print(self.av[self.pos[0],self.pos[1],0])
           print(self.next_pos)
        


    def step(self):
        if (np.random.rand() < 0.1):
            max_idx = np.random.randint(0,4)
        else:
            max_idx = np.argmax(self.av[self.pos[0],self.pos[1]])
        # print(f"{max_idx} is the max")
        match max_idx:
            case 0: #LEFT
                print("LEFT")
                self.next_pos = [self.pos[0],max(0,self.pos[1]-1)]
            case 1: #UP
                print("UP")
                self.next_pos = [max(0,self.pos[0]-1), self.pos[1]]
            case 2: #RIGHT
                print("RIGHT")
                self.next_pos = [self.pos[0],min(self.size-1,self.pos[1]+1)]
            case 3: #DOWN
                print("DOWN")
                self.next_pos = [min(self.size-1,self.pos[0]+1), self.pos[1]]
            case _:
                print("idk if this could be triggered, bravo")

        # reward = self.step_reward
        if(self.next_pos in self.pits):
            print(f"I fell in pit {self.next_pos} \n\n")
            self.av[self.pos[0],self.pos[1],max_idx] += ALPHA *  (self.pit_reward + (GAMMA * self.av[(self.next_pos[0],self.next_pos[1])].max()) - self.av[self.pos[0],self.pos[1],max_idx])
            self.pos = [0,0]
            return
        elif(self.next_pos == self.goal):
            print("I reached goal")
            self.goal_counter += 1
            self.av[self.pos[0],self.pos[1],max_idx] += ALPHA *  (self.goal_reward + (GAMMA * self.av[(self.next_pos[0],self.next_pos[1])].max()) - self.av[self.pos[0],self.pos[1],max_idx])
            self.pos = [0,0]
            return
            
        self.av[self.pos[0],self.pos[1],max_idx] += ALPHA *  (self.step_reward + (GAMMA * self.av[(self.next_pos[0],self.next_pos[1])].max()) - self.av[self.pos[0],self.pos[1],max_idx])

        self.pos = self.next_pos
        print(self.av[self.pos[0],self.pos[1],0])
        print(self.next_pos)
        print("\n")


 
env = GridWorld(size=5)

steps = 400
for i in range(steps):
    env.step()

print(f"reached {env.goal_counter} goals in {steps} steps")
