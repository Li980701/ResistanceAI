from ..random_agent import RandomAgent
import random

class GreedyAgent(RandomAgent):
    '''A sample implementation of a random agent in the game The Resistance'''

    def __init__(self, name='Greedy'):
        '''
        Initialises the agent.
        Nothing to do here.
        '''
        RandomAgent.__init__(self, name)


    def propose_mission(self, team_size, betrayals_required = 1):
        '''
        expects a team_size list of distinct agents with id between 0 (inclusive) and number_of_players (exclusive)
        to be returned. 
        betrayals_required are the number of betrayals required for the mission to fail.
        '''
        if self.is_spy() and betrayals_required > 1:
            team = list(random.sample(self.spy_list, betrayals_required))
        else:
            team = [self.player_number]
        while len(team)<team_size:
            agent = random.randrange(self.number_of_players)
            if agent not in team:
                team.append(agent)
        return team        

    def vote(self, mission, proposer):
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        The function should return True if the vote is for the mission, and False if the vote is against the mission.
        '''
        if self.player_number in mission:
            return True
        if self.is_spy():
            spy_set = set(self.spy_list)
            team_set = set(mission)
            return not team_set.isdisjoint(spy_set)
        return False


    def betray(self, mission, proposer):
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players, and include this agent.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        The method should return True if this agent chooses to betray the mission, and False otherwise. 
        By default, spies will betray 30% of the time. 
        '''
        if self.is_spy():
            return True
        else:
            return False

        



