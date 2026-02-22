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
    # Obtengo la meta del problema
    meta = getattr(problem, "goal", None)

    # Obtener la meta del problema en caso de NOne
    if meta is None and hasattr(problem, "getGoalState") and callable(problem.getGoalState):
        meta = problem.getGoalState()

    # Si no logro obtener meta, devuelvo 0 como si no tuviera heuristica 0
    if meta is None:
        return 0

    # Distancia Manhattan calculado como |x1-x2| + |y1-y2|
    x, y = state
    mx, my = meta
    return abs(x - mx) + abs(y - my)


def euclideanHeuristic(state, problem):
    """
    The Euclidean distance heuristic.
    """
    # Se obtiene la meta del problema
    meta = getattr(problem, "goal", None)
    if meta is None and hasattr(problem, "getGoalState") and callable(problem.getGoalState):
        meta = problem.getGoalState()

    # En tal caso de que la meta siga siendo None se retorna 0
    if meta is None:
        return 0

    # Distancia Euclidiana: raiz(dx^2 + dy^2)
    x, y = state
    mx, my = meta
    return math.sqrt((x - mx) ** 2 + (y - my) ** 2)


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
