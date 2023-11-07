from mesa import Agent

class TreeCell(Agent):
    """
        A tree cell.
        
        Attributes:
            x, y: Grid coordinates
            condition: Can be "Fine", "On Fire", or "Burned Out"
            unique_id: (x,y) tuple.

            unique_id isn't strictly necessary here, but it's good practice to give one to each agent anyway.
    """

    def __init__(self, pos, model):
        """
        Create a new tree.

        Args:
            pos: The tree's coordinates on the grid.
            model: standard model reference for agent.
        """
        super().__init__(pos, model)
        self.pos = pos
        self.condition = "Alive"
        self._next_condition = None

    def step(self):
        """
        A diferencia de la primera simulación, en este caso es necesario especificar
        los casos para cuadno las céclulas se encuentran tanto vivas como muertas,
        en cuanto a bajp qué condiciones transicionan al estado opuesto.
        """
        neighbors = []
        for neighbor in self.model.grid.iter_neighbors(self.pos, True):
            if (self.pos[1] == 49 and neighbor.pos[1] == 0) or self.pos[1] + 1 == neighbor.pos[1]:
                neighbors.append(neighbor)
        if self.condition == "Dead":
            if ((neighbors[0].condition == "Dead") and (neighbors[2].condition == "Alive")or
                (neighbors[0].condition == "Alive") and (neighbors[2].condition == "Dead")):
                self._next_condition = "Alive"
        if self.condition == "Alive":
            if ((neighbors[0].condition == "Dead") and (neighbors[2].condition == "Dead")or
                (neighbors[0].condition == "Alive") and (neighbors[2].condition == "Alive")):
                self._next_condition = "Dead"

    
    def advance(self):
        """
        Advance the model by one step.
        """
        if self._next_condition is not None:
            self.condition = self._next_condition