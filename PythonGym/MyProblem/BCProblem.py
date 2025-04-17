#import sys
#sys.path.insert(1, '../AStar')
from AStar.Problem import Problem
from MyProblem.BCNode import BCNode
from States.AgentConsts import AgentConsts
import sys
import numpy as np

#Clase que implementa el problema especifico que queremos resolver y que hereda de la calse
#Problema genérico.
class BCProblem(Problem):
    

    def __init__(self, initial, goal, xSize, ySize):
        super().__init__(initial, goal)
        self.map = np.zeros((xSize,ySize),dtype=int)
        self.xSize = xSize
        self.ySize = ySize

        self._distance_cache = None
        self._cache_goal_coords = None
    
    #inicializa un mapa con el mapa proveniente del entorno Vector => Matriz
    def InitMap(self,m):
        for i in range(len(m)):
            x,y = BCProblem.Vector2MatrixCoord(i,self.xSize,self.ySize)
            self.map[x][y] = m[i]

    #Muestra el mapa por consola
    def ShowMap(self):
        for j in range(self.ySize):
            s = ""
            for i in range(self.xSize):
                s += ("[" + str(i) + "," + str(j) + "," + str(self.map[i][j]) +"]")
            print(s)

    #Calcula la heuristica del nodo en base al problema planteado (Se necesita reimplementar)
    def Heuristic(self, node):
        goal_x = self.goal.x
        goal_y = self.goal.y
        if self._distance_cache is None or self._cache_goal_xy != (goal_x, goal_y):
            INF = float('inf')
            distances = np.full((self.xSize, self.ySize), INF)

            from collections import deque
            queue = deque()

            # distance to goal cell is zero
            distances[goal_x][goal_y] = 0
            queue.append((goal_x, goal_y))

            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

            # floodfill depending on goal cell
            while queue:
                current_x, current_y = queue.popleft()
                for dx, dy in directions:
                    new_x = current_x + dx
                    new_y = current_y + dy
                    
                    if (0 <= new_x < self.xSize and
                        0 <= new_y < self.ySize and
                        BCProblem.CanMove(self.map[new_x][new_y])):
                        # if shorter path exists, update distance
                        if distances[new_x][new_y] > distances[current_x][current_y] + 1:
                            distances[new_x][new_y] = distances[current_x][current_y] + 1
                            queue.append((new_x, new_y))

            # cache updated
            self._distance_cache = distances
            self._cache_goal_xy = (goal_x, goal_y)

        return self._distance_cache[node.x][node.y]



    
    #Genera la lista de sucesores del nodo (Se necesita reimplementar)
    def GetSucessors(self, node):
        successors = []
        x = node.x
        y = node.y
        #direcciones posibles
        directions = [(1,0),(-1,0),(0,1),(0,-1)]
        #iteramos por cada dirección
        for dx,dy in directions:
            #calculamos la nueva posición
            newX = x + dx
            newY = y + dy
            #si la nueva posición es válida, creamos un nodo y lo añadimos a la lista de sucesores
            if newX >= 0 and newX < self.xSize and newY >= 0 and newY < self.ySize:
                if BCProblem.CanMove(self.map[newX][newY]):
                    self.CreateNode(successors,node,newX,newY)
    
        return successors
    
    #métodos estáticos
    #nos dice si podemos movernos hacia una casilla, se debe poner el valor de la casilla como
    #parámetro
    @staticmethod
    def CanMove(value):
        return value != AgentConsts.UNBREAKABLE and value != AgentConsts.SEMI_UNBREKABLE and value != AgentConsts.SEMI_UNBREKABLE
    
    #convierte coordenadas mapa en formato vector a matriz
    @staticmethod
    def Vector2MatrixCoord(pos,xSize,ySize):
        x = pos % xSize
        y = pos // ySize #division entera
        return x,y

    #convierte coordenadas mapa en formato matriz a vector
    @staticmethod
    def Matrix2VectorCoord(x,y,xSize):
        return y * xSize + x
    
    #convierte coordenadas del mapa en coordenadas del entorno (World) (nótese que la Y está invertida)
    @staticmethod
    def MapToWorldCoord(x,y,ySize):
        xW = x * 2
        yW = (ySize - y - 1) * 2
        return xW, yW

    #convierte coordenadas del entorno (World) en coordenadas mapa (nótese que la Y está invertida)
    @staticmethod
    def WorldToMapCoord(xW,yW,ySize):
        x = xW // 2
        y = yW // 2
        y = ySize - y - 1
        return x, y
    
    #versión real del método anterior, que nos ayuda a buscar los centros de las celdas.
    #aqui nos dirá los decimales, es decir como de cerca estamos de la esquina superior derecha
    #un valor de 1.9,1.9 nos dice que estamos en la casilla 1,1 muy cerca de la 2,2
    #en realidad, lo que buscamos es el punto medio de la casilla, es decir la 1.5, 1.5 en el caso
    #de la casilla 1,1
    @staticmethod
    def WorldToMapCoordFloat(xW,yW,ySize):
        x = xW / 2
        invY = (ySize*2) - yW
        invY = invY / 2
        return x, invY

    #se utiliza para calcular el coste de cada elemento del mapa 
    @staticmethod
    def GetCost(value):
        if value == AgentConsts.UNBREAKABLE:
            return 1000
        elif value == AgentConsts.SEMI_UNBREKABLE:
            return 100
        elif value == AgentConsts.SEMI_BREKABLE:
            return 10
        elif value == AgentConsts.BRICK:
            return 1
        elif value == AgentConsts.NOTHING:
            return 1
        else:
            return 0
    
    #crea un nodo y lo añade a successors (lista) con el padre indicado y la posición x,y en coordenadas mapa 
    def CreateNode(self,successors,parent,x,y):
        value=self.map[x][y]
        g=BCProblem.GetCost(value)
        rightNode = BCNode(parent,g,value,x,y)
        rightNode.SetH(self.Heuristic(rightNode))
        successors.append(rightNode)

    #Calcula el coste de ir del nodo from al nodo to (Se necesita reimplementar)
    def GetGCost(self, nodeTo):
        return BCProblem.GetCost(nodeTo.value)