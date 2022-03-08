# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random
import util

from game import Agent
from pacman import GameState
from game import AgentState


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(
            gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(
            len(scores)) if scores[index] == bestScore]
        # Pick randomly among the best
        # chosenIndex = random.choice(bestIndices)
        chosenIndex = bestIndices[-1]

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [
            ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        # print('newGhost', newGhostStates)
        foodList = newFood.asList()
        ghostList = [ghostState.getPosition() for ghostState in newGhostStates]
        for (index, item) in enumerate(ghostList):
            if newPos == item and newScaredTimes[index] == 0:  # 表示ghost非scared
                # print('不能到鬼的地方去')
                return float('-inf')

        if newPos in foodList:
            return float('inf')

        # 求到最近food的曼哈顿距离
        min_dis_food = float('inf')
        for food in foodList:
            dis_temp = util.manhattanDistance(food, newPos)
            min_dis_food = dis_temp if dis_temp < min_dis_food else min_dis_food

        # 求到最近ghoast的曼哈顿距离
        min_dis_ghost = float('inf')
        for ghost in ghostList:
            dis_temp = util.manhattanDistance(ghost, newPos)
            min_dis_ghost = dis_temp if dis_temp < min_dis_ghost else min_dis_ghost

        return 0.5*min_dis_ghost/min_dis_food+childGameState.getScore()


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def checkState(self, state: GameState, depth: int) -> bool:
        if state.isWin() or state.isLose() or depth == self.depth:
            return True
        return False

    def valueFunc(self, state: GameState, agentIdx: int, depth: int) -> int:
        agentIdx = agentIdx % self.agentNum
        depth = (depth+1) if agentIdx == 0 else depth  # 如果是max层则加1
        if self.checkState(state, depth):
            return self.evaluationFunction(state)
        if agentIdx == 0:
            return self.maxValue(state, agentIdx, depth)
        else:
            return self.minValue(state, agentIdx, depth)

    def maxValue(self, state: GameState, agentIdx: int, depth: int) -> int:
        v = float('-inf')
        for action in state.getLegalActions(agentIdx):
            v = max(v, self.valueFunc(state.getNextState(
                agentIdx, action), (agentIdx+1), depth))
        return v

    def minValue(self, state: GameState, agentIdx: int, depth: int):
        v = float('inf')
        for action in state.getLegalActions(agentIdx):
            v = min(v, self.valueFunc(state.getNextState(
                agentIdx, action), (agentIdx+1), depth))
        return v

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        # print('agent num', gameState.getNumAgents())
        self.agentNum: int = gameState.getNumAgents()
        res = []
        for action in gameState.getLegalActions():
            nextState = gameState.getNextState(0, action)
            temp = {
                'action': action,
                'value': self.valueFunc(nextState, 1, 0)
            }
            res.append(temp)
        res.sort(key=lambda x: x['value'])
        return res[-1].get('action')


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def checkState(self, state: GameState, depth: int) -> bool:
        if state.isWin() or state.isLose() or depth == self.depth:
            return True
        return False

    def valueFunc(self, state: GameState, agentIdx: int, depth: int, alpha: int, beta: int) -> int:
        agentIdx = agentIdx % self.agentNum
        depth = (depth+1) if agentIdx == 0 else depth  # 如果是max层则加1
        if self.checkState(state, depth):
            return self.evaluationFunction(state)
        if agentIdx == 0:
            return self.maxValue(state, agentIdx, depth, alpha, beta)
        else:
            return self.minValue(state, agentIdx, depth, alpha, beta)

    def maxValue(self, state: GameState, agentIdx: int, depth: int, alpha: int, beta: int) -> int:
        v = float('-inf')
        for action in state.getLegalActions(agentIdx):
            v = max(v, self.valueFunc(state.getNextState(
                agentIdx, action), (agentIdx+1), depth, alpha, beta))
            if v > beta:
                return v
            alpha = max(alpha, v)
        return v

    def minValue(self, state: GameState, agentIdx: int, depth: int, alpha: int, beta: int):
        v = float('inf')
        for action in state.getLegalActions(agentIdx):
            v = min(v, self.valueFunc(state.getNextState(
                agentIdx, action), (agentIdx+1), depth, alpha, beta))
            if v < alpha:
                return v
            beta = min(beta, v)
        return v

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        self.agentNum: int = gameState.getNumAgents()
        res = []
        alpha = float('-inf')
        beta = float('inf')
        for action in gameState.getLegalActions():
            nextState = gameState.getNextState(0, action)
            temp = {
                'action': action,
                'value': self.valueFunc(nextState, 1, 0, alpha, beta)
            }
            alpha = max(alpha, temp['value'])
            res.append(temp)
        res.sort(key=lambda x: x['value'])
        return res[-1].get('action')


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction


class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()
