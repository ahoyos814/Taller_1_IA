from algorithms.problems import SearchProblem
import algorithms.utils as utils
from world.game import Directions
from algorithms.heuristics import nullHeuristic


def tinyHouseSearch(problem: SearchProblem):
    """
    Returns a sequence of moves that solves tinyHouse. For any other building, the
    sequence of moves will be incorrect, so only use this for tinyHouse.
    """
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
    # TODO: Add your code here
    utils.raiseNotDefined()


def breadthFirstSearch(problem: SearchProblem):
    """
    Search the shallowest nodes in the search tree first.
    """
    # TODO: Add your code here
    utils.raiseNotDefined()


def uniformCostSearch(problem: SearchProblem):
    """
    Search the node of least total cost first.
    """

    # TODO: Add your code here
    utils.raiseNotDefined()


def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    # Estado inicial del problema
    start_state = problem.getStartState()

    # Caso trivial: ya estamos en la meta
    if problem.isGoalState(start_state):
        return []

    # Frontera priorizada por f(n) = g(n) + h(n)
    frontier = utils.PriorityQueue()
    frontier.push((start_state, [], 0), heuristic(start_state, problem))

    # Mejor costo real g(n) encontrado hasta ahora para cada estado
    cost_so_far = {start_state: 0}

    while not frontier.isEmpty():
        state, path, path_cost = frontier.pop()

        # Ignoramos entradas obsoletas de la frontera (ya existe un mejor g para este estado)
        if path_cost > cost_so_far.get(state, float("inf")):
            continue

        # Cuando llegamos a meta, devolvemos la secuencia de acciones
        if problem.isGoalState(state):
            return path

        # Expandimos sucesores y relajamos costos
        for successor, action, step_cost in problem.getSuccessors(state):
            new_cost = path_cost + step_cost

            # Solo actualizamos si encontramos un camino más barato al sucesor
            if new_cost < cost_so_far.get(successor, float("inf")):
                cost_so_far[successor] = new_cost
                new_path = path + [action]
                priority = new_cost + heuristic(successor, problem)
                frontier.push((successor, new_path, new_cost), priority)

    # Si no hay solución alcanzable
    return []


# Abbreviations (you can use them for the -f option in main.py)
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
