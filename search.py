# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state: 'tuple[int,int]') -> bool:
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state: 'tuple[int,int]') -> 'tuple[tuple[int,int],str,int]':
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions: 'list[str]'):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    # '''
    visited: set = set()
    stack = util.Stack()
    step = 0
    res = []
    curState = {'state': problem.getStartState(), 'action': 'Stop',
                'accStepNum': step}

    stack.push(curState)
    while not stack.isEmpty():
        top = stack.pop()
        # print(top)
        visited.add(top['state'])
        step = top['accStepNum']
        step = step+1
        res = res[:top['accStepNum']-1]
        if top['accStepNum'] != 0:
            res.append(top['action'])

        if problem.isGoalState(top['state']):
            break

        succList = problem.getSuccessors(top['state'])
        for successor in succList:
            if successor[0] not in visited:
                stack.push(
                    {'state': successor[0], 'action': successor[1], 'accStepNum': step})

    return res
    # '''


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    visited: set = set()
    queue = util.Queue()
    res = []
    # print('kaishi', problem.getStartState())
    curState = {'state': problem.getStartState(), 'action': 'Stop',
                'route': []}

    queue.push(curState)
    # visited.add(curState['state'])
    i: int = 0
    while not queue.isEmpty():
        i = i+1
        front = queue.pop()
        if front['state'] in visited:
            continue
        if problem.isGoalState(front['state']):
            res = front['route']
            break

        visited.add(front['state'])
        succList = problem.getSuccessors(front['state'])
        for successor in succList:
            if successor[0] not in visited:
                queue.push(
                    {'state': successor[0], 'action': successor[1], 'route': front['route']+[successor[1]]})
                # visited.add(successor[0])

    # return ['West', 'West', 'West', 'South', 'South']
    # print('路线', res)
    return res


def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    # return ['West']
    visited: set = set()
    queue = util.PriorityQueue()
    res = []
    startState = {'state': problem.getStartState(), 'action': 'Stop',
                  'route': []}
    queue.push(startState, 0)
    # visited.add(startState['state'])
    while not queue.isEmpty():
        front = queue.pop()
        if front['state'] in visited:
            continue
        if problem.isGoalState(front['state']):
            res = front['route']
            break

        visited.add(front['state'])
        succList = problem.getSuccessors(front['state'])
        for successor in succList:
            if successor[0] not in visited:
                queue.push(
                    {'state': successor[0], 'action': successor[1], 'route': front['route']+[successor[1]]}, problem.getCostOfActions(front['route']+[successor[1]]))
                # visited.add(successor[0])
    return res


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    visited: set = set()
    queue = util.PriorityQueue()
    res = []
    startState = {'state': problem.getStartState(), 'action': 'Stop',
                  'route': []}
    queue.push(startState, 0+heuristic(startState['state'], problem))
    # visited.add(startState['state'])
    while not queue.isEmpty():
        front = queue.pop()
        if front['state'] in visited:
            continue
        if problem.isGoalState(front['state']):
            res = front['route']
            break

        visited.add(front['state'])
        succList = problem.getSuccessors(front['state'])
        for successor in succList:
            if successor[0] not in visited:
                queue.push(
                    {'state': successor[0],
                     'action': successor[1],
                     'route': front['route']+[successor[1]]
                     }, problem.getCostOfActions(front['route']+[successor[1]])+heuristic(successor[0], problem))
                # visited.add(successor[0])
    return res


def myHeuristic(state, problem):
    goal = problem.goal
    return util.manhattanDistance(state, goal)


def approxAStarSearch(problem, heuristic=myHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    visited: set = set()
    queue = util.PriorityQueue()
    res = []
    startState = {'state': problem.getStartState(), 'action': 'Stop',
                  'route': []}
    queue.push(startState, 0+heuristic(startState['state'], problem))
    # visited.add(startState['state'])
    while not queue.isEmpty():
        front = queue.pop()
        if front['state'] in visited:
            continue
        if problem.isGoalState(front['state']):
            res = front['route']
            break

        visited.add(front['state'])
        succList = problem.getSuccessors(front['state'])
        for successor in succList:
            if successor[0] not in visited:
                if problem.isGoalState(successor[0]):
                    res = front['route']+[successor[1]]
                    return res
                queue.push(
                    {'state': successor[0],
                     'action': successor[1],
                     'route': front['route']+[successor[1]]
                     }, problem.getCostOfActions(front['route']+[successor[1]])+heuristic(successor[0], problem))
    return res


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
