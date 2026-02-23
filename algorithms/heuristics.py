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
    #Versión 1
    #heuristica h(n) = max(manhattan(agente, sobrevivientes)) 
    """ 
     position, survivors_grid = state
    agent_x, agent_y = position
    
    max_distance = 0
    for x in range(survivors_grid.width):
        for y in range(survivors_grid.height):
            if survivors_grid[x][y]:  
                manhattan_dist = abs(agent_x - x) + abs(agent_y - y)
                max_distance = max(max_distance, manhattan_dist)
    
    return max_distance
    """
    #Versión 2
    # h(n) = min(manhattan(agente, sobreviviente)) + max(manhattan(agente, sobreviviente))
    
    """  
       position, survivors_grid = state
    agent_x, agent_y = position
    
    min_distance = float('inf')
    max_distance = 0
    
    for x in range(survivors_grid.width):
        for y in range(survivors_grid.height):
            if survivors_grid[x][y]:  
                manhattan_dist = abs(agent_x - x) + abs(agent_y - y)
                min_distance = min(min_distance, manhattan_dist)
                max_distance = max(max_distance, manhattan_dist)
    
    # If no survivors, return 0
    if min_distance == float('inf'):
        return 0
    
    return min_distance + max_distance
    """

    #Versión final
    # h(n) = distancia(agente, sobreviviente más cercano) + MST(sobrevivientes restantes)  
    
    position, survivors_grid = state
    agent_x, agent_y = position
    
    # Obtener la lista de sobrevivientes a partir de survivors_grid
    survivors = []
    for x in range(survivors_grid.width):
        for y in range(survivors_grid.height):
            if survivors_grid[x][y]:
                survivors.append((x, y))
    
    # Si no hay sobrevivientes, el costo es 0
    if not survivors:
        return 0
    
    # Calcular la distancia Manhattan al sobreviviente más cercano
    min_distance = float('inf')
    for survivor_x, survivor_y in survivors:
        dist = abs(agent_x - survivor_x) + abs(agent_y - survivor_y)
        min_distance = min(min_distance, dist)
    
    # Calcular el costo del MST de los sobrevivientes, usando caching para evitar cálculos repetidos
    tupla_survivors = tuple(sorted(survivors))
    if tupla_survivors not in problem.heuristicInfo:
        # Calcular MST usando Prim's algorithm
        if len(survivors) <= 1:
            mst_costos = 0
        else:
            visitados = {survivors[0]}
            mst_costos = 0
            
            while len(visitados) < len(survivors):
                min_edge = float('inf')
                next_survivor = None
                
                # Encontrar la frontera más barata que conecta un sobreviviente visitado con uno no visitado
                for v in visitados:
                    for u in survivors:
                        if u not in visitados:
                            dist = abs(v[0] - u[0]) + abs(v[1] - u[1])
                            if dist < min_edge:
                                min_edge = dist
                                next_survivor = u
                
                if next_survivor:
                    visitados.add(next_survivor)
                    mst_costos += min_edge
        
        problem.heuristicInfo[tupla_survivors] = mst_costos
    
    mst_costos = problem.heuristicInfo[tupla_survivors]
    
    return min_distance + mst_costos
