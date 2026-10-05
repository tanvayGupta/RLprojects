import numpy as np 
import math

np.random.seed(67)


def armRNG(arms=10):
    #I will create a hidden rewards array, it would be 2D. Each Index will have its mean and standard deviation. It will be a normal distribution
    # with mean randomly set from 0 to 1, and S.D. set randomly from 0.1 to 0.2
    x = np.array([np.round(np.random.rand(arms),3), 0.1 + np.round((np.random.rand(arms))/10,3)])

    return x


def RLagent(epsilon=0.1, arms=10, iterations=1000):
    hiddenRewards = armRNG(arms=arms)
    print("The hidden rewards are \n")
    print(hiddenRewards)
    print("\n\n")
    
    rewardArray = np.zeros(arms)
    iterationArray = np.ones(arms)

    for i in range(iterations):
        r = np.random.rand()
        if r <= epsilon : #Exploration
            rIndex = np.random.randint(0,arms) #r/epsilon gets it into the range 0 to 1, on which I can further multiply with arms to get index. Floored to ensure I dont have Indexoutofbounds
        else: #Exploitation
            rIndex = np.argmax(rewardArray)
        reward = np.clip(np.round(np.random.normal(loc=hiddenRewards[0][rIndex], scale = hiddenRewards[1][rIndex]),3),-1,1)
        rewardArray[rIndex] = rewardArray[rIndex] + ((reward-rewardArray[rIndex])/iterationArray[rIndex])
        iterationArray[rIndex] += 1

    print("This is the reward array created by the RL Agent")
    print(rewardArray)
            




    return "It's Done"

# print(armRNG())

print("\n\n --- OUTPUT LANE --- \n\n")

print(RLagent())