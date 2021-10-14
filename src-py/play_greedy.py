from resistance.random_agent import RandomAgent
from resistance.game import Game

from resistance.mct.greedy_agent import GreedyAgent

agents = [GreedyAgent(),
        RandomAgent(name='r2'),  
        RandomAgent(name='r3'),  
        RandomAgent(name='r4'),  
        RandomAgent(name='r5'),  
        RandomAgent(name='r6'),  
        RandomAgent(name='r7')]

game = Game(agents)
game.play()
print(game)


