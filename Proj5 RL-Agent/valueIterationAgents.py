# valueIterationAgents.py
# -----------------------
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

# valueIterationAgents.py
# -----------------------
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

from functools import reduce
import mdp, util

from learningAgents import ValueEstimationAgent
import collections


class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self,
                 mdp: mdp.MarkovDecisionProcess,
                 discount=0.9,
                 iterations=100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter()  # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        nextValues = self.values.copy()
        for i in range(self.iterations):
            # 对每个state进行更新
            for state in self.mdp.getStates():
                if self.mdp.isTerminal(state):
                    continue
                maxQValue = max(
                    map(lambda action: self.getQValue(state, action),
                        self.mdp.getPossibleActions(state)))
                nextValues[state] = maxQValue

            #因为采用batch，并且注意深拷贝
            self.values = nextValues.copy()

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def computeQValueFromValues(self, state, action) -> 'float':
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"

        def computeQ(stateAndProb: 'tuple'):
            nextState, prob = stateAndProb
            return prob * (self.mdp.getReward(state, action, nextState) +
                           self.discount * self.getValue(nextState))

        return reduce(
            lambda x, y: x + y,
            map(computeQ, self.mdp.getTransitionStatesAndProbs(state, action)))

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        qValues = util.Counter()
        for a in self.mdp.getPossibleActions(state):
            qValues[a] = self.getQValue(state, a)

        #如果没有可以迭代的actions，即qValues是空的，执行argMax会返回None
        return qValues.argMax()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)


class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount=0.9, iterations=1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        nextValues = self.values.copy()
        states = self.mdp.getStates()
        for i in range(self.iterations):
            # 对每个state进行更新
            state = states[i % len(states)]
            if self.mdp.isTerminal(state):
                continue
            maxQValue = max(
                map(lambda action: self.getQValue(state, action),
                    self.mdp.getPossibleActions(state)))
            self.values[state] = maxQValue


class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount=0.9, iterations=100, theta=1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        states = filter(lambda state: not self.mdp.isTerminal(state),
                        self.mdp.getStates())
        priorQ = util.PriorityQueue()

        predecessorDict: dict[tuple, set] = dict()
        for state in states:
            maxQValue = max(
                map(lambda action: self.getQValue(state, action),
                    self.mdp.getPossibleActions(state)))
            diff = abs(maxQValue - self.getValue(state))
            priorQ.update(state, -1 * diff)
            #找祖先
            for action in self.mdp.getPossibleActions(state):
                sucessors = list(
                    map(lambda x: x[0],
                        self.mdp.getTransitionStatesAndProbs(state, action)))
                for sucessor in sucessors:
                    if sucessor not in predecessorDict.keys():
                        predecessorDict[sucessor] = set()
                    predecessorDict[sucessor].add(state)
        for i in range(self.iterations):
            if priorQ.isEmpty():
                break

            state = priorQ.pop()
            #Update the value of s (if it is not a terminal state) in self.values
            maxQValue = max(
                map(lambda action: self.getQValue(state, action),
                    self.mdp.getPossibleActions(state)))
            self.values[state] = maxQValue
            #For each predecessor p of s, do
            for predecessor in predecessorDict[state]:
                maxQValue = max(
                    map(lambda action: self.getQValue(predecessor, action),
                        self.mdp.getPossibleActions(predecessor)))
                diff = abs(maxQValue - self.getValue(predecessor))
                if diff > self.theta:
                    priorQ.update(predecessor, -1 * diff)
