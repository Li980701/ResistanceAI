
from os import name
from resistance.game import Game
from resistance.mct.mct_agent import MCTAgent
from resistance.mct.li_agent import Agent
from resistance.mct.Beginer import Beginer
from resistance.random_agent import RandomAgent
from resistance.mct.greedy_agent import GreedyAgent
def test(n_game, players):

    scoreboard = {agent.name:{'spy':[0, 0], 'resistance':[0, 0], 'total':[0, 0]} for agent in players}

    mctnodes = MCTAgent.load('mctnodes_dict.json',)
    # mctnodes = {}
    for game_ind in range(n_game):
        print(game_ind, 'start')
        game = Game(players)

        for agent in game.agents:
            if type(agent) == MCTAgent:
                agent.mctNodes = mctnodes


        game.play()
        for agent in game.agents:
            if agent.name == "m1" or agent.name == "m2" or agent.name == "m3" or agent.name == "r1" or agent.name == "r2" or agent.name == "r3":
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
            if agent.name == "b1":
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
            if agent.name == "l1" or agent.name == 'l2' or agent.name == 'l3':
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

agents = [      
                MCTAgent(name='m1', sharedMctNodes={}, isTest=True), 
                MCTAgent(name='m2', sharedMctNodes={}, isTest=True), 
                RandomAgent(name = "r1"),
                RandomAgent(name = "r2"),
                RandomAgent(name = "r3"),
                # Agent(name = "l1"),
                # Agent(name = "l2"),
                # Agent(name = "l3"),
                
            
          ]
test(1000, agents)                



