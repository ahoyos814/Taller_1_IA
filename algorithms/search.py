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

    # =====================================================================
    # PRIMERA VERSION (sin IA)
    # la idea es como un bfs pero en vez de expandir por niveles
    # expandimos el nodo que tenga menor costo acumulado
    # usamos la PriorityQueue de utils para eso
    # =====================================================================
    #
    # inicio = problem.getStartState()
    #
    # # cola de prioridad, metemos el estado con su camino y costo
    # cola = utils.PriorityQueue()
    # cola.push((inicio, [], 0), 0)
    #
    # visitados = set()
    #
    # while not cola.isEmpty():
    #     nodo, acciones, costo = cola.pop()
    #
    #     if nodo in visitados:
    #         continue
    #
    #     visitados.add(nodo)
    #
    #     # si es la meta retornamos las acciones
    #     if problem.isGoalState(nodo):
    #         return acciones
    #
    #     # recorremos los vecinos
    #     for siguiente, accion, paso in problem.getSuccessors(nodo):
    #         if siguiente not in visitados:
    #             nuevo = costo + paso
    #             cola.push((siguiente, acciones + [accion], nuevo), nuevo)
    #
    # return []
    #
    # =====================================================================
    # FIN PRIMERA VERSION
    # =====================================================================

    # =====================================================================
    # PROMPT 1:
    # "tengo este codigo de uniform cost search pero tengo una duda,
    # que pasa si el robot ya esta en la posicion del sobreviviente
    # desde el inicio? y tambien, hay alguna forma de que sea mas
    # eficiente? porque con el set de visitados siento que podria
    # no encontrar el camino mas barato siempre"
    #
    # RESPUESTA IA:
    # - agregar chequeo al inicio por si el estado inicial ya es meta
    # - cambiar el set de visitados por un diccionario que guarde el
    #   mejor costo conocido, asi si encontramos un camino mas barato
    #   a un nodo lo podemos actualizar
    # =====================================================================

    # VERSION FINAL

    inicio = problem.getStartState()

    # chequeo edge case: si ya estamos en la meta no nos movemos
    if problem.isGoalState(inicio):
        return []

    # cola de prioridad, la prioridad es el costo acumulado
    cola = utils.PriorityQueue()
    cola.push((inicio, [], 0), 0)

    # en vez de un set usamos diccionario para guardar el mejor costo a cada nodo
    mejor_costo = {inicio: 0}

    while not cola.isEmpty():
        nodo, acciones, costo = cola.pop()

        # si ya hay un camino mas barato a este nodo, lo saltamos
        if costo > mejor_costo.get(nodo, float("inf")):
            continue

        if problem.isGoalState(nodo):
            return acciones

        for siguiente, accion, paso in problem.getSuccessors(nodo):
            nuevo_costo = costo + paso

            # solo lo metemos si es mejor que lo que ya teniamos
            if nuevo_costo < mejor_costo.get(siguiente, float("inf")):
                mejor_costo[siguiente] = nuevo_costo
                cola.push((siguiente, acciones + [accion], nuevo_costo), nuevo_costo)

    return []


def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    # Se pone el estado inicial
    inicio = problem.getStartState()

    # Caso donde ya estoy en la meta
    if problem.isGoalState(inicio):
        return []

    # frontera que evalua la prioridad de A* que es: g(n) + h(n)
    frontera = utils.PriorityQueue()
    frontera.push((inicio, [], 0), heuristic(inicio, problem))

    #Guarda el mejor costo que se puede obtener
    mejor_costo = {inicio: 0}

    while not frontera.isEmpty():
        estado, camino, costo_camino = frontera.pop()

        # En el caso de que sea peor que el mejor costo conocido no se expande
        if costo_camino > mejor_costo.get(estado, float("inf")):
            continue

        # si es la meta se retorna el camino
        if problem.isGoalState(estado):
            return camino

        # expanden los sucesores
        for sucesor, accion, costo_paso in problem.getSuccessors(estado):
            nuevo_costo = costo_camino + costo_paso

            # se actualiza si se encuentra un camino mejor
            if nuevo_costo < mejor_costo.get(sucesor, float("inf")):
                mejor_costo[sucesor] = nuevo_costo
                prioridad = nuevo_costo + heuristic(sucesor, problem)
                frontera.push((sucesor, camino + [accion], nuevo_costo), prioridad)

    # En tal caso de que no se encuentre solución, se retorna una lista vacía
    return []


# Abbreviations (you can use them for the -f option in main.py)
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
