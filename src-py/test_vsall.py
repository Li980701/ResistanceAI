

from resistance.game import Game
from resistance.mct.mct_agent import MCTAgent
from resistance.mct.li_agent import MAgent
from resistance.random_agent import RandomAgent



def test(n_game, players):

    scoreboard = {agent.name: {'spy': [0, 0], 'resistance': [
        0, 0], 'total': [0, 0]} for agent in players}

    # Loading pre-learned dictionary 
    mctnodes = MCTAgent.load('mctnodes_dict.json',)

    # Not loading
    # mctnodes = {}
    for game_ind in range(n_game):
        print(game_ind, 'start')
        game = Game(players)

        for agent in game.agents:
            if type(agent) == MCTAgent:
                agent.mctNodes = mctnodes

        game.play()
        for agent in game.agents:
            if agent.name == "m1" or agent.name == "m2" or agent.name == "m3" or agent.name == "r1" or agent.name == "r2":
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
                if agent.is_spy:
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

# Hybrid mode open 
# agents = [
#     RandomAgent(name="r1"),
#     RandomAgent(name='r2'),
#     MCTAgent(name='m1', sharedMctNodes={}, isTest=True),
#     MCTAgent(name='m2', sharedMctNodes={}, isTest=True),
#     MCTAgent(name='m3', sharedMctNodes={}, isTest=True),
# ]

# Model based agent
# agents = [
#     RandomAgent(name="r1"),
#     RandomAgent(name='r2'),
#     MAgent(name="l1"),
#     MAgent(name="l2"),
#     MAgent(name="l3"),
# ]

# Hybrid close
agents = [
    RandomAgent(name="r1"),
    RandomAgent(name='r2'),
    MCTAgent(name='m1', sharedMctNodes={}, isTest=False),
    MCTAgent(name='m2', sharedMctNodes={}, isTest=False),
    MCTAgent(name='m3', sharedMctNodes={}, isTest=False),
]
test(80000, agents)
