import random
class Agent:
    '''An abstract super class for an agent in the game The Resistance.
    new_game and *_outcome methods simply inform agents of events that have occured,
    while propose_mission, vote, and betray require the agent to commit some action.'''

    #game parameters for agents to access
    #python is such that these variables could be mutated, so tournament play
    #will be conducted via web sockets.
    #e.g. self.mission_size[8][3] is the number to be sent on the 3rd mission in a game of 8
    mission_sizes = {
            5:[2,3,2,3,3], \
            6:[3,3,3,3,3], \
            7:[2,3,3,4,5], \
            8:[3,4,4,5,5], \
            9:[3,4,4,5,5], \
            10:[3,4,4,5,5]
            }
    #number of spies for different game sizes
    spy_count = {5:2, 6:2, 7:3, 8:3, 9:3, 10:4} 
    #e.g. self.betrayals_required[8][3] is the number of betrayals required for the 3rd mission in a game of 8 to fail
    fails_required = {
            5:[1,1,1,1,1], \
            6:[1,1,1,1,1], \
            7:[1,1,1,2,1], \
            8:[1,1,1,2,1], \
            9:[1,1,1,2,1], \
            10:[1,1,1,2,1]
            }

    i_won_as_resis   = False
    i_won_as_spies   = False 

    def __init__(self, name):
        self.name             = name
        self.I_am_Spy         = False
        self.id               = -1
        self.rounds_completed = 0
        self.num_of_players   = 0
        self.spies_has_won    = 0
        self.resis_has_won    = 0
        self.num_of_spies     = 0
        self.current_round    = 0
        self.suspects_value   = {}
        self.votes            = []
        self.game_history     = []
        self.spies            = []

    def __str__(self):
        return 'Agent '+self.name

    def __repr__(self):
        return self.__str__()

    def new_game(self, number_of_players, player_number, spies):
        self.num_of_players = number_of_players
        self.id             = player_number
        self.spies          = spies
        self.num_of_spies   = self.spy_count[self.num_of_players]
        self.I_am_Spy = True if self.id in spies else False
        for i in range(self.num_of_players):
                self.suspects_value[i] = 0

    def suspects(self, instructions):
        ans = []
        temp = dict(sorted(self.suspects_value.items(), key = lambda item:item[1]))
        # instruction = 0: return a list of players with least suspect values
        if instructions == 0:
            temp = list(temp)
            ans = temp[:self.num_of_spies]
        # instructions = 1: return a list of players with highest suspect values
        elif instructions == 1:
            temp = list(temp)
            temp.reverse()
            ans = temp[:self.num_of_spies + 1]    
        else:
            ans = list(temp)
        
        return ans

    def propose_mission(self, team_size, fails_required = 1):
        # whatever roles I play in this game,
        # I always want me in the mission
        # because I am confident in my loyalty
        team       = []
        resistance = []
        team.append(self.id)
        if self.I_am_Spy:
            fails = 1
            if fails_required > 1:
                # I want a spy that has less suspects_value
                # to mess with other players' head
                player = self.suspects(2)
                while fails < fails_required:
                    for p in player:
                        if p in self.spies:
                            if p != self.id:
                                team.append(p)
                                fails += 1
                        else:
                            resistance.append(p)
            else:
                while len(team) < team_size:
                    for i in range(self.num_of_players):
                        if i not in self.spies:
                            team.append(i)
            j = 0
            while len(team) < team_size:
                if j not in self.spies:
                    team.append(resistance[j])
                j += 1
        else:
            if self.rounds_completed == 0:
                while len(team) < team_size:
                    team.append(random.randint(0, self.num_of_players - 1))
            else:
                # find players that are trustworthy atm
                player = self.suspects(2)
                for i in range(self.num_of_players):
                    team.append(player[i])
        return team

    def vote(self, mission, proposer):
        if self.rounds_completed == self.current_round:
            self.current_round += 1
        fails_required = self.fails_required[self.num_of_players][self.current_round - 1]
        if self.current_round == 1:
            return True
        if not self.I_am_Spy:
            suspects = self.suspects(1)
            if len(list(set(suspects) & set(mission))) > 0:
                return False
        else:
            if self.current_round >= 3:
                return False
        return True

    def vote_outcome(self, mission, proposer, votes):
        round_vote = []
        for i in range(self.num_of_players):
            if i in votes:
                round_vote.append(True)
            else:
                round_vote.append(False)
        self.votes.append(round_vote)
        
    def betray(self, mission, proposer):
        if self.current_round == 1:
            return False
        spies_on_mission = list((set(self.spies) & set(mission)))
        fail_required = self.fails_required[self.num_of_players][self.current_round - 1]

        if len(spies_on_mission) < fail_required:
            return False
        else:
            if len(spies_on_mission) > fail_required:
                if self.current_round < 3:
                    return False
        return True

    def mission_outcome(self, mission, proposer, num_fails, mission_success):
        self.game_history.append([mission, mission_success])
        if self.current_round == 1:
            return
        if not mission_success:
            self.suspects_value[proposer] += 1
            for player in mission:
                self.suspects_value[player] += 1
            for voter_choices in self.votes:
                if voter_choices is True:
                    self.suspects_value[voter_choices] += 1
        else:
            for voter_choices in self.votes:
                if voter_choices is False:
                    self.suspects_value[voter_choices] += 1






        # if mission_success:
        #     if num_fails == 0:
        #         self.suspects_value[proposer] -= 5
        #     else:
        #         self.suspects_value[proposer] -= 2
        #     for i in mission:
        #         if num_fails == 0:
        #             if self.current_round == 1:
        #                 self.suspects_value[i] -= 2
        #             else:
        #                 self.suspects_value[i] -= 10
        #     for j in range(self.num_of_players):
        #         if self.votes[self.current_round - 1][j] is False:
        #             self.suspects_value[j] += 10
        #         else:
        #             self.suspects_value[j] -= 10
                
        # else:
        #     if num_fails > 1:
        #         self.suspects_value[proposer] += 10
        #     else:
        #         self.suspects_value[proposer] += 5
        #     for i in mission:
        #         if self.current_round == 1:
        #             self.suspects_value[i] += 5
        #         else:
        #             self.suspects_value[i] += 10
        #     for j in range(self.num_of_players):
        #         if self.votes[self.current_round - 1][j] is True:
        #             self.suspects_value[j] += 8
        #         else:
        #             self.suspects_value[j] -= 10
        
        # for p in range(self.num_of_players):
        #     count_good = 0
        #     count_bad = 0
        #     participation = 0
        #     for r in range(len(self.game_history)):
        #         if p in self.game_history[r][0]:
        #             participation += 1
        #             if self.game_history[r][1]:
        #                 count_good += 1
        #             else:
        #                 count_bad += 1
        #     if count_good >= participation / 2:
        #         self.suspects_value[p] -= 8
        #     if count_bad >= participation / 2:
        #         self.suspects_value[p] += 10
                    
        # for p in range(self.num_of_players):
        #     count_good = 0
        #     count_bad = 0
        #     for r in range(len(self.game_history)):
        #         if self.game_history[r][1] == self.votes[r][p]:
        #             count_good += 1
        #         else:
        #             count_bad += 1
        #     if count_good >= self.current_round / 2:
        #          self.suspects_value[p] -= 6
        #     if count_bad >= self.current_round / 2:
        #         self.suspects_value[p] += 8
                          
                  
    def round_outcome(self, rounds_complete, missions_failed):
        self.rounds_completed = rounds_complete
        self.spies_has_won = missions_failed
        self.resis_has_won = rounds_complete - missions_failed
    
    def game_outcome(self, resistance_win, spies):
        if resistance_win:
            if not self.I_am_Spy:
                self.i_won_as_resis = True

        else:
            if self.I_am_Spy:
                self.i_won_as_spies = True

        return self.i_won_as_resis, self.i_won_as_spies











        # if self.current_round == 1:
        #     for i in range(self.num_of_players):
        #         self.suspects_value[i] = 0
        # self.game_history.append((mission, proposer, mission_success))
        # fail_required = self.fails_required[self.num_of_players][self.current_round - 1]
        # if mission_success:
        #     if self.current_round != 1:
        #         if fail_required > 1:
        #             self.suspects_value[proposer] -= 5
        #         for player in mission:
        #             if num_fails == 0:
        #                 self.suspects_value[player] -= 5
        #             else:
        #                 self.suspects_value[player] += 1
        #         for i in range(self.num_of_players):
        #             if self.votes[self.current_round - 1][i] is False:
        #                 self.suspects_value[i] += 2
        #             else:
        #                 self.suspects_value[i] -= 2
        # else:
        #     if self.current_round != 1:
        #         if num_fails > 1:
        #             self.suspects_value[proposer] += 5
        #         else:
        #             self.suspects_value[proposer] += 2
        #         for player in mission:
        #             self.suspects_value[player] += 5

        #     else:
        #         self.suspects_value[proposer] += 1
        #         for player in mission:
        #             self.suspects_value[player] += 5





        # self.game_history.append((mission, proposer, mission_success))
        # fail_required = self.fails_required[self.num_of_players][self.current_round - 1]
        # if mission_success:
        #     if self.current_round != 1:
        #         if fail_required > 1:
        #             self.suspects_value[proposer] -= 5
        #         for player in mission:
        #             if num_fails == 0:
        #                 self.suspects_value[player] -= 5
        #             else:
        #                 for j in mission:
        #                     count = 0
        #                     count2 = 0
        #                     in_game = 0
        #                     for rounds in self.game_history:
        #                         if j in rounds[0]:
        #                             in_game += 1
        #                             if rounds[2] is True:
        #                                 count += 1
        #                             else:
        #                                 count2 += 1
        #                     if count >= in_game / 2:
        #                         self.suspects_value[j] -= 2
        #                     if count2 >= in_game / 2:
        #                         self.suspects_value[j] += 2

        #         for players in range(self.num_of_players):
        #             count = 0
        #             count2 = 0
        #             for i in range(len(self.votes)):
        #                 if self.game_history[i][2] == self.votes[i][players]:
        #                     count += 1
        #                 else:
        #                     count2 += 1
        #             if count >= self.current_round / 2:
        #                 self.suspects_value[players] -= 2
        #             if count2 >= self.current_round / 2:
        #                 self.suspects_value[players] += 2
        # else:
        #     if self.current_round != 1:
        #         if num_fails > 1:
        #             self.suspects_value[proposer] += 5
        #         else:
        #             self.suspects_value[proposer] += 2
        #         for j in mission:
        #             count = 0
        #             count2 = 0
        #             in_game = 0
        #             for rounds in self.game_history:
        #                 if j in rounds[0]:
        #                     in_game += 1
        #                     if rounds[2] is True:
        #                         count += 1
        #                     else:
        #                         count2 += 1
        #             if count >= in_game / 2:
        #                 self.suspects_value[j] -= 2
        #             if count2 >= in_game / 2:
        #                 self.suspects_value[j] += 2
        #         for players in range(self.num_of_players):
        #             count = 0
        #             count2 = 0
        #             for i in range(len(self.votes)):
        #                 if self.game_history[i][2] != self.votes[i][players]:
        #                     count += 1
        #                 else:
        #                     count2 += 1
        #             if count >= self.current_round / 2:
        #                 self.suspects_value[players] += 2
        #             if count2 >= self.current_round / 2:
        #                 self.suspects_value[players] -= 2
        #     else:
        #         self.suspects_value[proposer] += 1
        #         for player in mission:
        #             self.suspects_value[player] += 5


