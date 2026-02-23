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
    # Pila LIFO: expande primero el nodo más profundo descubierto.
    frontera = utils.Stack()
    estado_inicial = problem.getStartState()

    # Cada elemento de la frontera es: (estado, lista_de_acciones_hasta_ese_estado).
    frontera.push((estado_inicial, []))

    # Conjunto de estados ya expandidos para evitar ciclos.
    visitados = set()

    while not frontera.isEmpty():
        # Sacamos el último estado agregado a la pila.
        estado, acciones = frontera.pop()

        # Si alcanzamos la meta, devolvemos el camino de acciones.
        if problem.isGoalState(estado):
            return acciones

        # Si ya se expandió este estado, lo saltamos.
        if estado in visitados:
            continue

        # Marcamos como visitado justo cuando lo expandimos.
        visitados.add(estado)

        # Agregamos sucesores no visitados para seguir profundizando.
        for sucesor, accion, _ in problem.getSuccessors(estado):
            if sucesor not in visitados:
                frontera.push((sucesor, acciones + [accion]))

    # Si no hay solución, retornamos lista vacía.
    return [] 


def breadthFirstSearch(problem: SearchProblem):
    """
    Search the shallowest nodes in the search tree first.
    """
    # Cola FIFO: expande primero los nodos más cercanos al estado inicial.
    frontera = utils.Queue()
    estado_inicial = problem.getStartState()

    # Cada elemento de la frontera es: (estado, lista_de_acciones_hasta_ese_estado).
    frontera.push((estado_inicial, []))

    # En BFS marcamos visitado al encolar para no duplicar estados en la cola.
    visitados = {estado_inicial}

    while not frontera.isEmpty():
        # Sacamos el estado más antiguo en la cola (orden por niveles).
        estado, acciones = frontera.pop()

        # Si llegamos al objetivo, devolvemos el camino de acciones.
        if problem.isGoalState(estado):
            return acciones

        # Expandimos sucesores no visitados y los encolamos al final.
        for sucesor, accion, _ in problem.getSuccessors(estado):
            if sucesor not in visitados:
                visitados.add(sucesor)
                frontera.push((sucesor, acciones + [accion]))

    # Si no existe solución, retornamos lista vacía.
    return []


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

      # =====================================================================
    # PRIMERA VERSION (la de prueba, bien basica)
    # la idea era simple:
    # A* escoge el nodo con menor valor de f(n) = g(n) + h(n)
    # g(n) = costo acumulado
    # h(n) = heuristica
    # =====================================================================
    #
    # inicio = problem.getStartState()
    #
    # # cola con prioridad para sacar siempre el que tenga menor f
    # cola = utils.PriorityQueue()
    # cola.push((inicio, [], 0), heuristic(inicio, problem))
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
    #     # si llegamos al objetivo devolvemos el camino
    #     if problem.isGoalState(nodo):
    #         return acciones
    #
    #     # expandimos vecinos
    #     for siguiente, accion, paso in problem.getSuccessors(nodo):
    #         if siguiente not in visitados:
    #             nuevo_costo = costo + paso
    #             prioridad = nuevo_costo + heuristic(siguiente, problem)
    #             cola.push((siguiente, acciones + [accion], nuevo_costo), prioridad)
    #
    # return []
    #
    # =====================================================================
    # FIN PRIMERA VERSION
    # =====================================================================

    # =====================================================================
    # PROMPT 1:
    # "oye, el A* ya corre pero me surgieron dos cositas:
    #  1) si apenas arranca ya estamos en la meta, igual deberia buscar?
    #  2) con visitados como set, no se me puede quedar por fuera
    #     un camino mas barato que aparezca despues?"
    #
    # RESPUESTA IA:
    # - hacer validacion al inicio: si inicio ya es meta, devolver []
    # - cambiar visitados(set) por mejor_costo(dict)
    # - si llega un estado con costo peor al guardado, se descarta
    # - si llega con mejor costo, se actualiza y se mete otra vez en la cola
    # =====================================================================

    # VERSION FINAL


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
