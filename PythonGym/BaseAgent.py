import random
import time
class BaseAgent:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    #Devuelve el nombre del agente
    def Name(self):
        return self.name
    #Devuelve el id del agente
    def Id(self):
        return self.id
    #Metodo que se llama al iniciar el agente. No devuelve nada y sirve para contruir el agente
    def Start(self):
        print("Inicio del agente ")

    #Metodo que se llama en cada actualización del agente, y se proporciona le vector de percepciones
    #Devuelve la acción u el disparo si o no
    def Update(self, perception,map):
        print("Toma de decisiones del agente")
        print(perception)
        print("Mapa")
        print(map)
        action = random.randint(0,4)
        return action, True
    
    def print_perception(self, perception):
        labels = ["NEIGHBORHOOD_UP",
                  "NEIGHBORHOOD_DOWN",
                  "NEIGHBORHOOD_RIGHT",
                  "NEIGHBORHOOD_LEFT",
                  "NEIGHBORHOOD_DIST_UP",
                  "NEIGHBORHOOD_DIST_DOWN",
                  "NEIGHBORHOOD_DIST_RIGHT",
                  "NEIGHBORHOOD_DIST_LEFT",
                  "PLAYER_X",
                  "PLAYER_Y",
                  "COMMAND_CENTER_X",
                  "COMMAND_CENTER_Y",
                  "AGENT_X",
                  "AGENT_Y",
                  "CAN_FIRE",
                  "HEALTH",
                  "LIFE_X",
                  "LIFE_Y",	
                  "TIME"]

        for label, val in zip(labels, perception):
            print(label, val)
    
    #Metodo que se llama al finalizar el agente, se pasa el estado de terminacion
    def End(self, win):
        print("Agente finalizado")
        print("Victoria ",win)