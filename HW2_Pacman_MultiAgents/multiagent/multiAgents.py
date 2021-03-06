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
        some Directions.X for some X in the set {North, South, West, East, Stop}
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
        if currentGameState.isWin():
            return successorGameState.getScore()
        score = 0
        #weight of getting food
        flist = newFood.asList()
        if currentGameState.getNumFood() > len(flist):
            score = 0
        else:
            flag = 10000 #a flag to find the closest food
            for food in flist:
                fooddist = manhattanDistance(food, newPos)
                if fooddist < flag:
                    flag = fooddist
            score = flag

            
        #weight of gost distance
        curGhostPos = currentGameState.getGhostState(1).getPosition()
        newGhostPos = successorGameState.getGhostState(1).getPosition()
        for ghost in newGhostStates:
            score = score + 4 ** (2 - manhattanDistance(newGhostPos, newPos))
            
        if action == Directions.STOP:
            score = score + 3
            
        capsules = successorGameState.getCapsules()
        clist = capsules
        if len(currentGameState.getCapsules()) == len(clist):
            flag = 10000 #a flag to find the closest food
            for food in clist:
                fooddist = manhattanDistance(food, newPos)
                if fooddist < flag:
                    flag = fooddist
            score = score + flag

        return -score
        #return successorGameState.getScore() #default scoure
        #please change the return score as the score you want

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
        """
        "*** YOUR CODE HERE ***"
        def minmax(state, depth, agentcode):
            if state.isWin() or state.isLose():
                return state.getScore()
            
            action = state.getLegalActions(agentcode)
            agentnum = state.getNumAgents()
            step = Directions.STOP
            
            if agentcode == 0:
                maxima = -float('inf')
                for act in action:
                    evaluation = minmax(state.generateSuccessor(agentcode, act), depth, 1)
                    maxima = max(maxima, evaluation)
                    if maxima == evaluation:
                        step = act
                if depth == self.depth -1:
                    return step
                return maxima
            
            elif agentcode > 0 and agentcode < agentnum - 1:
                minima = float('inf')
                for act in action:
                    evaluation = minmax(state.generateSuccessor(agentcode, act), depth, agentcode + 1)
                    minima = min(minima, evaluation)
                return minima
            
            elif agentcode > 0 and agentcode == agentnum - 1:
                minima = float('inf')
                for act in action:
                    if depth == 0:
                        evaluation =  self.evaluationFunction(state.generateSuccessor(agentcode, act))
                    else:
                        evaluation = minmax(state.generateSuccessor(agentcode, act), depth - 1, 0)
                    minima = min(minima, evaluation)
                return minima
                    
        return minmax(gameState, self.depth-1, 0)
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def minmax(state, depth, agentcode, alpha, beta):
            if state.isWin() or state.isLose():
                return state.getScore()
            
            action = state.getLegalActions(agentcode)
            agentnum = state.getNumAgents()
            step = Directions.STOP
            
            if agentcode == 0:
                maxima = -float('inf')
                for act in action:
                    evaluation = minmax(state.generateSuccessor(agentcode, act), depth, 1, alpha, beta)
                    maxima = max(maxima, evaluation)
                    if maxima == evaluation:
                        step = act
                    
                    alpha = max(alpha, maxima)
                    if alpha > beta:
                        break
                if depth == self.depth -1:
                    return step
                return maxima
            
            elif agentcode > 0 and agentcode < agentnum - 1:
                minima = float('inf')
                for act in action:
                    evaluation = minmax(state.generateSuccessor(agentcode, act), depth, agentcode + 1, alpha, beta)
                    minima = min(minima, evaluation)
                    beta = min(beta, minima)
                    if beta < alpha:
                        break
                return minima
            
            elif agentcode > 0 and agentcode == agentnum - 1:
                minima = float('inf')
                for act in action:
                    if depth == 0:
                        evaluation =  self.evaluationFunction(state.generateSuccessor(agentcode, act))
                    else:
                        evaluation = minmax(state.generateSuccessor(agentcode, act), depth - 1, 0, alpha, beta)
                        
                    minima = min(minima, evaluation)
                    beta = min(beta, minima)
                    if beta < alpha:
                        break
                return minima
                    
        return minmax(gameState, self.depth-1, 0, -float('inf'), float('inf'))
        util.raiseNotDefined()

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
        def minmax(state, depth, agentcode):
            if state.isWin() or state.isLose():
                return state.getScore()
            
            action = state.getLegalActions(agentcode)
            agentnum = state.getNumAgents()
            step = Directions.STOP
            probability = 1.0 / len(action)
            
            if agentcode == 0:
                maxima = -float('inf')
                for act in action:
                    evaluation = minmax(state.generateSuccessor(agentcode, act), depth, 1)
                    maxima = max(maxima, evaluation)
                    if maxima == evaluation:
                        step = act
                if depth == self.depth -1:
                    return step
                return maxima
            
            elif agentcode > 0 and agentcode < agentnum - 1:
                score = 0.0
                for act in action:
                    evaluation = minmax(state.generateSuccessor(agentcode, act), depth, agentcode + 1)
                    score = score + probability * evaluation
                return score
            
            elif agentcode > 0 and agentcode == agentnum - 1:
                score = 0.0
                for act in action:
                    if depth == 0:
                        evaluation =  self.evaluationFunction(state.generateSuccessor(agentcode, act))
                    else:
                        evaluation = minmax(state.generateSuccessor(agentcode, act), depth - 1, 0)
                    score = score + probability * evaluation
                return score
                    
        return minmax(gameState, self.depth-1, 0)
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

