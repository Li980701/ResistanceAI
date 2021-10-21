import copy
from math import log, sqrt


def getIndexOfList(l):
    '''
    Get the index of list l
    '''
    k = 1
    ret = 0
    for s in l:
        ret += s * k
        k *= 10
    return str(ret)


def getPropose(childrenDict, startIndex, playerSize, prefix, missionSize):
    '''
    Do a total Permutation when a preposed is needed 
    '''
    if startIndex + missionSize > playerSize:
        return
    elif missionSize == 0:
        childrenDict[getIndexOfList(prefix)] = [0, 0]
        return
    else:
        for i in range(startIndex, playerSize):
            newPrefix = copy.deepcopy(prefix) + (i,)
            getPropose(childrenDict, i+1, playerSize, newPrefix, missionSize-1)


class BaseNode:
    '''
    File node is the structure of the MCT tree
    Three types of nodes: Voting Node, Propose Node and Betray Node
    Action Decision Function: chooseAction(), designed with UBC function with Constance C value 1.0 by default
    '''
    @staticmethod
    def chooseAction(children, c):
        n = 0
        for key in children:
            if children[key][1] == 0 :
                return key, 0
                # N is how many times of visiting times of current node
            n += children[key][1]
        log_n = log(n)
        # UCB function, balance exploitation and exploration 
        l = [((children[key][0] / children[key][1] + c * sqrt(log_n /  children[key][1])), key) for key in children]
        l.sort()
        # retrieve the action(True or False)
        action = l[-1][1]
        # Winning times / Total visited times
        return action, children[key][0] / children[key][1]

    @staticmethod
    def createVoteNode():
        children = {
            True: [0, 0],
            False: [0, 0]
        }
        return children

    @staticmethod
    def createProposeNode(missionSize, playerSize):
        children = {}
        getPropose(children, 0, playerSize, (), missionSize)
        return children

    @staticmethod
    def createBetrayNode():
        children = {
            True: [0, 0],
            False: [0, 0]
        }
        return children



            