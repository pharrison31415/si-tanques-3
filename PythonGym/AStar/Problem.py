class Problem:
    
    def __init__(self, initial, goal):
        self.initial = initial
        self.goal = goal

    def Initial(self):
        return self.initial
    
    #I think this will verify if the node is the goal-node (defined in SetGoal), that has the hugest possible g and h=0
    def IsASolution(self, node):
        return node == self.goal

    #we can do floodfill here
    #Calcula la heuristica del nodo en base al problema planteado (Se necesita reimplementar)
    def Heuristic(self, node):
        raise NotImplementedError("Heuristic no implementado")
        return 0.0

    #Genera la lista de sucesores del nodo (Se necesita reimplementar)
    #this would be the posssible neighboors of the actual node or floodfill values in up, down, left and right positions from the actual node 
    def GetSucessors(self, node):
        raise NotImplementedError("GetSucessors no implementado")
        return []

    #Calcula el coste de ir del nodo from al nodo to (Se necesita reimplementar)
    #la diferencia entre el g(actual) y el g(sucesor) -> 1, puede haber diferencia de coste a depender de los bloques.
    def GetGCost(self, nodeTo):
        raise NotImplementedError("GetGCost no implementado")
        return 0.0

    #this can be fighting the player, going for cc or getting the life 
    def SetGoal(self, goal):
        self.goal = goal

    #initial node?
    def SetInitial(self, initial):
        self.initial = initial

    #this is the present goal node, depending on the present set of the enviroment (perception)
    def GetGoal(self):
        return self.goal

