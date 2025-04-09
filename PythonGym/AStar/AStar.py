#Algoritmo A* genérico que resuelve cualquier problema descrito usando la plantilla de la
#la calse Problem que tenga como nodos hijos de la clase Node

from States.AgentConsts import AgentConsts 
class AStar:

    def __init__(self, problem):
        self.open = [] # lista de abiertos o frontera de exploración
        self.processed = set() # set, conjunto de cerrados (más eficiente que una lista)
        self.problem = problem #problema a resolver

    def GetPlan(self):
        #for seted goal, ellaborate the path with the minimum cost to the goal, and return the path in the right order
        findGoal = False
        #TODO implementar el algoritmo A*

        #cosas a tener en cuenta:
        #Si el número de sucesores es 0 es que el algoritmo no ha encontrado una solución, devolvemos el path vacio []
        #Hay que invertir el path para darlo en el orden correcto al devolverlo (path[::-1])
        #GetSucesorInOpen(sucesor) nos devolverá None si no lo encuentra, si lo encuentra
        #es que ese sucesor ya está en la frontera de exploración, DEBEMOS MIRAR SI EL NUEVO COSTE ES MENOR QUE EL QUE TENIA ALMACENADO
        #SI esto es asi, hay que cambiarle el padre y setearle el nuevo coste.
        self.open.clear()
        self.processed.clear()
        self.open.append(self.problem.Initial())
        path = []
        while self.open:
            
            self.open.sort(key=lambda x: x.F()) #ordenamos la lista de abiertos por el coste total (G+H)
            current_node = self.open.pop(0)

            #si el nodo actual es la meta, reconstruimos el path y lo devolvemos ##borrar esta parte y poner para devolver path cuando no hay mas abiertos
            if current_node.x == AgentConsts.AGENT_X and current_node.y == AgentConsts.AGENT_Y:
                path = self.ReconstructPath(current_node)
                return path
            

            for successor in self.problem.GetSucessors(current_node):
                #si el sucesor no está en la lista de abiertos, lo añadimos
                if successor not in self.open and successor not in self.processed:
                    self.open.append(successor)
                    self._ConfigureNode(successor,current_node,current_node.G()+self.problem.GetGCost(successor))
                else:
                    #si el sucesor ya está en abiertos, miramos si el nuevo coste es menor que el que tenía
                    found = self.GetSucesorInOpen(successor)
                    if found != None and current_node.G() + self.problem.GetGCost(successor) < found.G():
                        #si es menor, lo actualizamos y le cambiamos el padre
                        self._ConfigureNode(found,current_node,current_node.G()+self.problem.GetGCost(successor))

            self.processed.add(current_node)

        #mientras no encontremos la meta y haya elementos en open....
        #TODO implementar el bucle de búsqueda del algoritmo A*
        return path

    #nos permite configurar un nodo (node) con el padre y la nueva G
    def _ConfigureNode(self, node, parent, newG):
        node.SetParent(parent)
        node.SetG(newG)
        node.SetH(self.problem.Heuristic(node))

    #nos dice si un sucesor está en abierta. Si esta es que ya ha sido expandido y tendrá un coste, comprobar que le nuevo camino no es más eficiente
    #En caso de serlos, _ConfigureNode para setearle el nuevo padre y el nuevo G, asi como su heurística
    def GetSucesorInOpen(self,sucesor):
        i = 0
        found = None
        while found == None and i < len(self.open):
            node = self.open[i]
            i += 1
            if node == sucesor:
                found = node
        return found


    #reconstruye el path desde la meta encontrada.
    def ReconstructPath(self, goal):
        path = []
        current_node = goal
        while current_node != None:
            path.append(current_node)
            current_node = current_node.GetParent()
        return path[::-1]
    