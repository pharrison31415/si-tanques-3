import random
from States.AgentConsts import AgentConsts

class GoalMonitor:

    GOAL_COMMAND_CENTRER = 0
    GOAL_LIFE = 1
    GOAL_PLAYER = 2
    def __init__(self, problem, goals):
        self.goals = goals
        self.problem = problem
        self.lastTime = -1
        self.recalculate = False

    def ForceToRecalculate(self):
        self.recalculate = True

    #determina si necesitamos replanificar
    def NeedReplaning(self, perception, map, agent):
        if self.recalculate:
            self.lastTime = perception[AgentConsts.TIME]
            return True
        
        #si el tiempo ha pasado más de 10 segundos, se fuerza la replanificación
        if perception[AgentConsts.TIME] - self.lastTime > 10:
            self.lastTime = perception[AgentConsts.TIME]
            return True
        
        #si el agente tiene 1 vida, se fuerza la replanificación
        if perception[AgentConsts.LIFE] <= 1:
            self.lastTime = perception[AgentConsts.TIME]
            return True
        
        

        return False
    
    #selecciona la meta mas adecuada al estado actual
    def SelectGoal(self, perception, map, agent):
        goal_distances = [ abs(g.x - agent.x) + abs(g.y - agent.y) for g in self.goals ]
        min_distance = min(goal_distances)
        min_distance_index = goal_distances.index(min_distance)
        return self.goals[min_distance_index]
    
    def UpdateGoals(self,goal, goalId):
        self.goals[goalId] = goal
