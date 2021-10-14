"""
run the file by `python3 src-py/test_1m4r.py`

[with pretrain & in train mode]: MCTAgent(name='m1', sharedMctNodes={}, isTest=False),
r2 {'spy': [14, 40], 'resistance': [37, 60], 'total': [51, 100]}
r3 {'spy': [15, 50], 'resistance': [28, 50], 'total': [43, 100]}
r4 {'spy': [16, 43], 'resistance': [36, 57], 'total': [52, 100]}
m1 {'spy': [21, 35], 'resistance': [49, 65], 'total': [70, 100]}
r5 {'spy': [8, 32], 'resistance': [39, 68], 'total': [47, 100]}

[with pretrain in test mode (boost by greedy)]: MCTAgent(name='m1', sharedMctNodes={}, isTest=true),
r3 {'spy': [11, 39], 'resistance': [33, 61], 'total': [44, 100]}
r2 {'spy': [11, 39], 'resistance': [33, 61], 'total': [44, 100]}
m1 {'spy': [29, 41], 'resistance': [49, 59], 'total': [78, 100]}
r5 {'spy': [13, 40], 'resistance': [34, 60], 'total': [47, 100]}
r4 {'spy': [14, 41], 'resistance': [34, 59], 'total': [48, 100]}


"""

from resistance.game import Game
from resistance.random_agent import RandomAgent
from resistance.mct.mct_agent import MCTAgent
from resistance.mct.li_agent import Agent
from resistance.mct.greedy_agent import GreedyAgent
import json


def test(n_game, players):

    scoreboard = {agent.name: {'spy': [0, 0], 'resistance': [0, 0], 'total': [0, 0]} for agent in players}

    mctnodes = {}
    # mctnodes = MCTAgent.load('mctnodes_dict.json',)

    for game_ind in range(n_game):
        print(game_ind, 'start')
        game = Game(players)

        for agent in game.agents:
            if type(agent) == MCTAgent:
                agent.mctNodes = mctnodes

        game.play()
        for agent in game.agents:
            if agent.name == 'm1' or agent.name == 'm2' or agent.name == 'm3' or agent.name == 'g1' or agent.name == 'g2' or agent.name == 'g3':
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
            else:
                if agent.I_am_Spy:
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

# agents = [MCTAgent(name='m1', sharedMctNodes={}, isTest=False),
#         MCTAgent(name='m2', sharedMctNodes={}, isTest=False),
#         MCTAgent(name='m3', sharedMctNodes={}, isTest=False),
#         Agent(name='l4'),
#         Agent(name='l5'),
#         Agent(name='l6'),
#         ]


# agents = [MCTAgent(name='m1', sharedMctNodes={}, isTest=False),
#           MCTAgent(name='m2', sharedMctNodes={}, isTest=False),
#           MCTAgent(name='m3', sharedMctNodes={}, isTest=False),
#           Agent(name='l1'),
#           Agent(name='l2'),
#           Agent(name='l3'),
#           ]
agents = [MCTAgent(name='m1', sharedMctNodes={}, isTest=True), 
          Agent(name='l1'),
          Agent(name='l2'),
          Agent(name='l3'),
          Agent(name='l4'),
          Agent(name='l5'),
          Agent(name='l6'),
          Agent(name='l7'),
          Agent(name='l8'),
          ]

test(10000, agents)
