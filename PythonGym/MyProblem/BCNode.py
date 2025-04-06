from AStar.Node import Node

#Clase que implementa un nodo de BattleCity
#A parte de los datos por defecto, implementamos el método 
#IsEqual que nos ayudará a detectar cuando dos nosdos son iguales
class BCNode(Node):
    def __init__(self, parent, g, value, x, y):
        super().__init__(parent, g)
        self.value = value
        self.x = int(x)
        self.y = int(y)
    
    def __repr__(self):
        return f"BCNode(x={self.x}, y={self.y})"

    def __eq__(self, other):
        if other == None:
            return False
        conditions = [
            self.x == other.x,
            self.y == other.y,
            self.value == other.value,
        ]
        return all(conditions)

    def __hash__(self):
        return hash((self.x, self.y))
