
from resistance.game import Game
from resistance.mct.mct_agent import MCTAgent
from resistance.mct.greedy_agent import GreedyAgent
from resistance.mct.Beginer import Beginer

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
            if agent.name == "m1":
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
            if agent.name == "b1" or agent.name == "b2" or agent.name == "b3" or agent.name == "b4":
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
          Beginer(name='b1'),  
          Beginer(name='b2'),  
          Beginer(name='b3'),  
          Beginer(name='b4'),
        ]

test(100, agents)                



