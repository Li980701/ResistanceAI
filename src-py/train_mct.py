"""
run the file by `python3 src-py/train_mct.py`
"""

from os import name
from resistance.game import Game
from resistance.mct.mct_agent import MCTAgent
from resistance.mct.li_agent import Agent
from resistance.mct.Beginer import Beginer
from resistance.random_agent import RandomAgent
from resistance.mct.greedy_agent import GreedyAgent
from resistance.mct.Bounder import Bounder
import json
import time

def mix_pretrain(n_game):

    shared_dict = {}
    # 4 of players boost by Random
    # players = [MCTAgent(name='m1', sharedMctNodes=shared_dict, isTest=True), 
    #            RandomAgent(name = "r1"),
    #            RandomAgent(name = "r2"),
    #            RandomAgent(name = "r3"),
    #            RandomAgent(name = "r4"),
    #       ]

    # 4 Greedy play boost random
    # players = [MCTAgent(name='m1', sharedMctNodes=shared_dict, isTest=False), 
    #             RandomAgent(name = "r1"),
    #             RandomAgent(name = "r2"),
    #             RandomAgent(name = "r3"),
    #             RandomAgent(name = "r4"),
    #       ]
    # players = [
    #       MCTAgent(name='m1', sharedMctNodes={}, isTest=False),
    #       MCTAgent(name='m2', sharedMctNodes={}, isTest=False), 
    #       MCTAgent(name='m3', sharedMctNodes={}, isTest=False),
    #       Bounder(name='r1'),  
    #       Bounder(name='r2'),  
    #       Bounder(name='r3')
    # ]
    players = [ MCTAgent(name='m1', sharedMctNodes={}, isTest=False), 
                MCTAgent(name='m2', sharedMctNodes={}, isTest=False), 
                RandomAgent(name = "r1"),
                RandomAgent(name = "r2"),
                RandomAgent(name = "r3"),
          ]
    last_save = time.time()

    

    scoreboard = {agent.name:{'spy':[0, 0], 'resistance':[0, 0], 'total':[0, 0]} for agent in players}

    for game_ind in range(n_game):
        game = Game(players)

        # before play, recovery from copy.deepcopy of agent
        for agent in game.agents:
            agent.mctNodes = shared_dict

        game.play()

        # update score board
        for agent in game.agents:
            if agent.name == 'm1' or agent.name == 'm2' or agent.name == 'm3' or agent.name == 'r1' or agent.name == 'r2' or agent.name == 'r3' or agent.name == 'r4':
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
            if agent.name == 'l1':
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
            
            if ((game_ind+1) % 50 == 0):
                print(agent.name, scoreboard[agent.name])

        if time.time() - last_save > 60:
            last_save = time.time()
            MCTAgent.save('mctnodes_dict.json', shared_dict)
    
    MCTAgent.save('mctnodes_dict.json', shared_dict)



mix_pretrain(1000)