"""
run the file by `python3 src-py/test_1g4r.py`
the score board for 100 games 
r5 {'spy': [12, 28], 'resistance': [43, 72], 'total': [55, 100]}
r2 {'spy': [14, 44], 'resistance': [29, 56], 'total': [43, 100]}
g1 {'spy': [32, 45], 'resistance': [46, 55], 'total': [78, 100]}
r4 {'spy': [13, 45], 'resistance': [27, 55], 'total': [40, 100]}
r3 {'spy': [11, 38], 'resistance': [32, 62], 'total': [43, 100]}
"""

from resistance.game import Game
from resistance.random_agent import RandomAgent
from resistance.mct.greedy_agent import GreedyAgent


def test(n_game, players):

    scoreboard = {agent.name:{'spy':[0, 0], 'resistance':[0, 0], 'total':[0, 0]} for agent in players}

    for game_ind in range(n_game):
        print(game_ind, 'start')
        game = Game(players)
        game.play()
        for agent in game.agents:
            if agent.is_spy():
                scoreboard[agent.name]['spy'][1] += 1
                scoreboard[agent.name]['total'][1] += 1

                if game.missions_lost >= 3:
                    scoreboard[agent.name]['spy'][0] += 1
                    scoreboard[agent.name]['total'][0] += 1
            else:
                scoreboard[agent.name]['resistance'][1] += 1
                scoreboard[agent.name]['total'][1] += 1

                if game.missions_lost < 3:
                    scoreboard[agent.name]['resistance'][0] += 1
                    scoreboard[agent.name]['total'][0] += 1
            
            print(agent.name, scoreboard[agent.name])

agents = [GreedyAgent(name='g1'), 
        RandomAgent(name='r2'),  
        RandomAgent(name='r3'),  
        RandomAgent(name='r4'),  
        RandomAgent(name='r5')]

test(100, agents)                



