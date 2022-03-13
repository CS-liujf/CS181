# logicPlan.py
# ------------
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
In logicPlan.py, you will implement logic planning methods which are called by
Pacman agents (in logicAgents.py).
"""

from re import L
import util
import sys
import logic
import game


pacman_str = 'P'
ghost_pos_str = 'G'
ghost_east_str = 'GE'
pacman_alive_str = 'PA'

class PlanningProblem:
    """
    This class outlines the structure of a planning problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the planning problem.
        """
        util.raiseNotDefined()

    def getGhostStartStates(self):
        """
        Returns a list containing the start state for each ghost.
        Only used in problems that use ghosts (FoodGhostPlanningProblem)
        """
        util.raiseNotDefined()
        
    def getGoalState(self):
        """
        Returns goal state for problem. Note only defined for problems that have
        a unique goal state such as PositionPlanningProblem
        """
        util.raiseNotDefined()

def tinyMazePlan(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def sentence1():
    """Returns a logic.Expr instance that encodes that the following expressions are all true.
    
    A or B
    (not A) if and only if ((not B) or C)
    (not A) or (not B) or C
    """
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    A = logic.Expr('A')
    B = logic.Expr('B')
    C = logic.Expr('C')
    A_or_B = (A|B)
    not_B_or_C= ((~B)|C)
    not_A_iff_not_B_or_C=((~A) % not_B_or_C)
    not_A_or_not_B_or_C=(logic.disjoin([(~A),(~B),(C)]))
    return logic.conjoin(A_or_B,not_A_iff_not_B_or_C,not_A_or_not_B_or_C)

def sentence2():
    """Returns a logic.Expr instance that encodes that the following expressions are all true.
    
    C if and only if (B or D)
    A implies ((not B) and (not D))
    (not (B and (not C))) implies A
    (not D) implies C
    """
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    A=logic.Expr('A')
    B=logic.Expr('B')
    C=logic.Expr('C')
    D=logic.Expr('D')
    C_iff_BorD=(C%(B|D))
    A_imp_notB_and_notD=(A>>((~B)&(~D)))
    not_Band_notC_imp_A=((~(B&(~C)))>> A)
    notD_imp_C=((~D)>>C)
    return logic.conjoin(C_iff_BorD,A_imp_notB_and_notD,not_Band_notC_imp_A,notD_imp_C)

def sentence3():
    """Using the symbols WumpusAlive[1], WumpusAlive[0], WumpusBorn[0], and WumpusKilled[0],
    created using the logic.PropSymbolExpr constructor, return a logic.PropSymbolExpr
    instance that encodes the following English sentences (in this order):

    The Wumpus is alive at time 1 if and only if the Wumpus was alive at time 0 and it was
    not killed at time 0 or it was not alive and time 0 and it was born at time 0.

    The Wumpus cannot both be alive at time 0 and be born at time 0.

    The Wumpus is born at time 0.
    """
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    alive_1=logic.PropSymbolExpr('WumpusAlive',1)
    alive_0=logic.PropSymbolExpr('WumpusAlive',0)
    born_0=logic.PropSymbolExpr('WumpusBorn',0)
    killed_0=logic.PropSymbolExpr('WumpusKilled',0)
    encode_1=(alive_1%((alive_0&(~killed_0))|((~alive_0)&born_0)))
    encode_2=(~(alive_0&born_0))
    encode_3=(born_0)
    return logic.conjoin(encode_1,encode_2,encode_3)

def findModel(sentence):
    """Given a propositional logic sentence (i.e. a logic.Expr instance), returns a satisfying
    model if one exists. Otherwise, returns False.
    """
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    cnf_form=logic.to_cnf(sentence)
    return logic.pycoSAT(cnf_form)

def atLeastOne(literals) :
    """
    Given a list of logic.Expr literals (i.e. in the form A or ~A), return a single 
    logic.Expr instance in CNF (conjunctive normal form) that represents the logic 
    that at least one of the literals in the list is true.
    >>> A = logic.PropSymbolExpr('A');
    >>> B = logic.PropSymbolExpr('B');
    >>> symbols = [A, B]
    >>> atleast1 = atLeastOne(symbols)
    >>> model1 = {A:False, B:False}
    >>> print logic.pl_true(atleast1,model1)
    False
    >>> model2 = {A:False, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    >>> model3 = {A:True, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    """
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    return logic.disjoin(literals)


def atMostOne(literals:list) :
    """
    Given a list of logic.Expr literals, return a single logic.Expr instance in 
    CNF (conjunctive normal form) that represents the logic that at most one of 
    the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    temp=[]
    for idx1,item1 in enumerate(literals):
        for idx2,item2 in enumerate(literals):
            if idx1<idx2:
                temp.append(logic.disjoin(~item1,~item2))
    
    return logic.conjoin(temp)


def exactlyOne(literals:list) :
    """
    Given a list of logic.Expr literals, return a single logic.Expr instance in 
    CNF (conjunctive normal form)that represents the logic that exactly one of 
    the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    return atLeastOne(literals)&atMostOne(literals)

def extractActionSequence(model:dict, actions:'list[str]'):
    """
    Convert a model in to an ordered list of actions.
    model: Propositional logic model stored as a dictionary with keys being
    the symbol strings and values being Boolean: True or False
    Example:
    >>> model = {"North[3]":True, "P[3,4,1]":True, "P[3,3,1]":False, "West[1]":True, "GhostScary":True, "West[3]":False, "South[2]":True, "East[1]":False}
    >>> actions = ['North', 'South', 'East', 'West']
    >>> plan = extractActionSequence(model, actions)
    >>> print plan
    ['West', 'South', 'North']
    """
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    temp=[]
    for key,value in model.items():
        act = logic.PropSymbolExpr.parseExpr(key)[0]
        if act in actions and value is True:
            t = int(logic.PropSymbolExpr.parseExpr(key)[1])
            temp.append((act,t))

    temp.sort(key=lambda x:x[1])
    res=list(map(lambda x:x[0],temp))
    return res

def pacmanSuccessorStateAxioms(x, y, t, walls_grid):
    """
    Successor state axiom for state (x,y,t) (from t-1), given the board (as a 
    grid representing the wall locations).
    Current <==> (previous position at time t-1) & (took action to move to x, y)
    """
    "*** YOUR CODE HERE ***"
    # return logic.Expr('A') # Replace this with your expression
    prev_state = [((x-1,y),'East'),((x+1,y),'West'),((x,y+1),'South'),((x,y-1),'North')]
    pre_liter_list =[]
    for state in prev_state:
        if not walls_grid[state[0][0]][state[0][1]]:
            temp = logic.PropSymbolExpr(pacman_str,state[0][0], state[0][1], t-1) & logic.PropSymbolExpr(state[1], t-1)
            pre_liter_list.append(temp)
    current=logic.PropSymbolExpr(pacman_str,x,y,t)
    return current%logic.disjoin(pre_liter_list)

def positionLogicPlan(problem):
    """
    Given an instance of a PositionPlanningProblem, return a list of actions that lead to the goal.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    walls = problem.walls
    width, height = problem.getWidth(), problem.getHeight()
    
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


def foodLogicPlan(problem):
    """
    Given an instance of a FoodPlanningProblem, return a list of actions that help Pacman
    eat all of the food.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    walls = problem.walls
    width, height = problem.getWidth(), problem.getHeight()

    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
plp = positionLogicPlan
flp = foodLogicPlan

# Some for the logic module uses pretty deep recursion on long expressions
sys.setrecursionlimit(100000)
    