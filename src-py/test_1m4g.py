"""
run the file by `python3 src-py/test_1m4r.py`

[with pretrain]: the score board for 100 games  --> cannot KO the greedy
g3 {'spy': [39, 39], 'resistance': [1, 61], 'total': [40, 100]}
g5 {'spy': [37, 37], 'resistance': [1, 63], 'total': [38, 100]}
g2 {'spy': [42, 43], 'resistance': [0, 57], 'total': [42, 100]}
m1 {'spy': [39, 39], 'resistance': [1, 61], 'total': [40, 100]}
g4 {'spy': [41, 42], 'resistance': [0, 58], 'total': [41, 100]}
"""

from resistance.game import Game
from resistance.mct.mct_agent import MCTAgent
from resistance.mct.greedy_agent import GreedyAgent


def test(n_game, players):

    scoreboard = {agent.name:{'spy':[0, 0], 'resistance':[0, 0], 'total':[0, 0]} for agent in players}

    mctnodes = MCTAgent.load('mctnodes_dict.json',)

    for game_ind in range(n_game):
        print(game_ind, 'start')
        game = Game(players)

        for agent in game.agents:
            if type(agent) == MCTAgent:
                agent.mctNodes = mctnodes


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

agents = [MCTAgent(name='m1', sharedMctNodes={}, isTest=False),
        GreedyAgent(name='g2'),  
        GreedyAgent(name='g3'),  
        GreedyAgent(name='g4'),  
        GreedyAgent(name='g5'),]

test(1000, agents)                



