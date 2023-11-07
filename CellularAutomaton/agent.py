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
        If the tree is on fire, spread it to fine trees nearby.
        """
        #Para las columnas que no están en las orillas, se checan los vecinos de arriba
        if self.condition == "Dead" and self.pos[1] < 49 and self.pos[0] > 0 and self.pos[0] < 49:
            neighbors = []
            #Se checan los vecinos de arriba
            for neighbor in self.model.grid.iter_neighbors(self.pos, True):
                #Si el vecino está en la fila de arriba en las posiciones de arriba a la izquierda, directamente arriba
                # o arriba a la derecha, se agrega a la lista de vecinos
                if neighbor.pos[1] == self.pos[1] + 1:
                    neighbors.append(neighbor)
            #Si se cumple con la condición de que el de la izquierda está muerto y el de la derecha vivo, o viceversa, entonces el vecino del centro recibe la condición de vivo
            if ((neighbors[0].condition == "Dead" and neighbors[2].condition == "Alive") or (neighbors[0].condition == "Alive" and neighbors[2].condition == "Dead")):
                self._next_condition = "Alive"
    
    def advance(self):
        """
        Advance the model by one step.
        """
        if self._next_condition is not None:
            self.condition = self._next_condition