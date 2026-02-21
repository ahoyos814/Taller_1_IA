import math
from typing import Any, Tuple
from algorithms import utils
from algorithms.problems import MultiSurvivorProblem


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def manhattanHeuristic(state, problem):
    """
    The Manhattan distance heuristic.
    """
    # Intentamos obtener la meta desde el problema (SimpleSurvivorProblem usa problem.goal)
    goal = None
    if hasattr(problem, "goal"):
        goal = problem.goal
    elif hasattr(problem, "getGoalState") and callable(problem.getGoalState):
        goal = problem.getGoalState()

    # Si por alguna razón no hay meta disponible, devolvemos heurística neutra
    if goal is None:
        return 0

    # Distancia Manhattan: movimientos ortogonales en grilla
    x, y = state
    goal_x, goal_y = goal
    return abs(x - goal_x) + abs(y - goal_y)


def euclideanHeuristic(state, problem):
    """
    The Euclidean distance heuristic.
    """
    # Intentamos obtener la meta desde el problema
    goal = None
    if hasattr(problem, "goal"):
        goal = problem.goal
    elif hasattr(problem, "getGoalState") and callable(problem.getGoalState):
        goal = problem.getGoalState()

    # Si no hay meta definida, no estimamos costo restante
    if goal is None:
        return 0

    # Distancia Euclidiana: línea recta entre estado actual y objetivo
    x, y = state
    goal_x, goal_y = goal
    return math.sqrt((x - goal_x) ** 2 + (y - goal_y) ** 2)


def survivorHeuristic(state: Tuple[Tuple, Any], problem: MultiSurvivorProblem):
    """
    Your heuristic for the MultiSurvivorProblem.

    state: (position, survivors_grid)
    problem: MultiSurvivorProblem instance

    This must be admissible and preferably consistent.

    Hints:
    - Use problem.heuristicInfo to cache expensive computations
    - Go with some simple heuristics first, then build up to more complex ones
    - Consider: distance to nearest survivor + MST of remaining survivors
    - Balance heuristic strength vs. computation time (do experiments!)
    """
    # TODO: Add your code here
    utils.raiseNotDefined()
