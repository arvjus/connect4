# Learning to play Connect 4 with Reinforcement Machine Learning

I wrote some software to play Connect 4 game with Reinforcement Machine Learning. 

## Quick overview

There are several agents to train/test my model:
  * Random - very weak player, selects random valid move
  * Simple - look for move that can end current game
  * One Step Look Ahead - heuristic helps to choose next move
  * N-Steps Look Ahead - implements minimax algorithm. currently it's slow
  * CNN (convolutional neural network) uses keras/tensorflow
  
You can install dependencies and try it by executing one of these files:
  * training.py - to train model. it take some time. learning_rate.py help to visualize learning process
  * tournament.py - two agents competes with each other
  * connect4_agent.py - two selected agents competes with each other (gui)
  * connect4_human.py - selected agent plays with human player (gui)

## Game window  
  
![Game window](https://github.com/arvjus/connect4/blob/main/images/gui-screenshot.png)

## Training of network  

I stardet model training with range of agents from weak to more complex and was quite surprised to see how quickly CNNAgent started to win. 
But even after relatively little training model could win against 3-steps minimax algorithm, when I played against model I could easily win. It looks like we need longer training cycle in order to train competitive player.   

![Learning rate](https://github.com/arvjus/connect4/blob/main/images/learning_rate.png)

## Further improvements

There are few things I should try in order to improve model:
  * More learning - keep playing with the same agent until winning rate reaches 0.85-0.9 before jumping to the next level
  * Change network model (deeper/wider)
  * Implement Monte Carlo Tree Search agent and train network against it.
  * Train network against itself
