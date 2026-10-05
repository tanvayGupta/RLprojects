# Hello There
So the 10 armed bandit project is the classic RL starting point.

What we have here is a simple model, which chooses between exploitation and exploration

Exploitation means choosing the option which is known to yield the best results and exploration means taking a gamble.
This gamble may result in getting a better yield in the future.

Epsilon is the split of exploration. Epsilon 0.1 would imply 10% exploration and 90% exploitation rate.

The only thing different from the classical n-bandit problem is that I have assigned each arm a random mean and standard deviation.
So the arms have a fixed mean and standard deviation per run.

And with this, I create a normal distribution, so that if a particular arm (say arm 4) is picked twice, it doesnt return the same value...

## Issues with this first version
well, 
**Firstly** I am using np.argmax
This means if 2 or more arms yield the same result, im not picking the arm randomly, I'm choosing the one with the lower index.
Right now, I don't feel it creates too much of a problem when iterations are high enough, but initially, it creates a 0-bias

As in, initially all rewards are 0, so we pick the 0th index, which always gives a positive reward
To fix this i just clipped it -1 to 1, instead of 0 to 1. This doesnt tackle the core of the problem but frankly, it's just luck, so exploration will figure the better way anyhow given enough iterations.

*Secondly*, while this is more of a lack=of-feature than a bug, I am not tracking this anywhere, so its boring to look at these matrices. Although the matrices are looking promising. "Hey Claude given this script, generate me a csv logger and a plotter.py script so I feel super proud of the 30-minute code I wrote"
