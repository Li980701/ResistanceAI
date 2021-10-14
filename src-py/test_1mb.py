from resistance.game import Game
from resistance.random_agent import RandomAgent
from resistance.mct.mct_agent import MCTAgent
from resistance.mct.Bounder import Bounder
import json


def test(n_game, players):

    scoreboard = {agent.name:{'spy':[0, 0], 'resistance':[0, 0], 'total':[0, 0]} for agent in players}

    # mctnodes = {}
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

agents = [MCTAgent(name='m1', sharedMctNodes={}, isTest=True),
          MCTAgent(name='m2', sharedMctNodes={}, isTest=True),  
          MCTAgent(name='m3', sharedMctNodes={}, isTest=True),  
          MCTAgent(name='m4', sharedMctNodes={}, isTest=True),
          MCTAgent(name='m5', sharedMctNodes={}, isTest=True),  
          Bounder(name='b1'),  
          Bounder(name='b2'),
          Bounder(name='b3'),
          Bounder(name='b4'),
          Bounder(name='b5'),
          ]

test(1000, agents)                