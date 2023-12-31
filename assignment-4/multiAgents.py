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
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def min(state):
            # Termination state
            if state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            # Keep track of how many agents have made an action
            self.turn += 1

            best = 100000
            # Look at all of the ghost's moves
            for action in state.getLegalActions(self.turn):
                next = state.generateSuccessor(self.turn, action)

                val = None
                # if everyone has made their turn, call max
                if self.turn == next.getNumAgents() - 1:
                    val = max(next)
                    # Reset turn after getting out of max
                    self.turn = next.getNumAgents() - 1
                else:
                    val = min(next)
                # Get max value of min() and current best
                best = val if val < best else best
            self.turn -= 1
            return best

        def max(state):
            self.turn = 0

            # Termination state
            if self.depth == 1 or state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            self.depth -= 1

            best = -1000000
            # Look at all of pacman's moves
            for action in state.getLegalActions(self.turn):
                next = state.generateSuccessor(self.turn, action)
                # Get max value of min() and current best
                val = min(next)
                best = val if val > best else best

            self.depth += 1
            return best

        # Compile results per action
        results = []
        for action in gameState.getLegalActions(self.index):
            self.turn = 0
            next = gameState.generateSuccessor(self.index, action)
            results.append((action, min(next)))

        # (Action, Score)
        argmax = (None, -1000000)
        for action, score in results:
            argmax = (action, score) if score > argmax[1] else argmax
        return argmax[0]


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        # I was not able to make the strategy I used for Minimax to work for
        # Alpha Beta pruning, mainly because it was so messy. Therefore, I
        # implemented a base minimax over again after doing some more research,
        # and added alpha-beta pruning to that.
        def minimax(state, agent, depth, alpha, beta):
            is_depth_reached = depth == self.depth * state.getNumAgents()
            if is_depth_reached or state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            if agent == 0:
                return maxval(state, agent, depth, alpha, beta)[1]
            else:
                return minval(state, agent, depth, alpha, beta)[1]

        def maxval(state, agent, depth, alpha, beta):
            v = (None, -1000000)
            for action in state.getLegalActions(agent):
                next = state.generateSuccessor(agent, action)
                val = minimax(next, (agent+1) % state.getNumAgents(), depth+1, alpha, beta)
                v = max(v, (action, val), key=lambda x: x[1])

                # This is the extra pruning part
                if v[1] > beta:
                    return v
                alpha = max(alpha, v[1])
            return v

        def minval(state, agent, depth, alpha, beta):
            v = (None, 1000000)
            for action in state.getLegalActions(agent):
                next = state.generateSuccessor(agent, action)
                val = minimax(next, (agent+1) % state.getNumAgents(), depth+1, alpha, beta)
                v = min(v, (action, val), key=lambda x: x[1])

                # This is the extra pruning part
                if v[1] < alpha:
                    return v
                beta = min(beta, v[1])
            return v

        return maxval(gameState, self.index, 0, -1000000, 1000000)[0]


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
