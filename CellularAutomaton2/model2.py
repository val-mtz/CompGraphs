import mesa
from mesa import Model, DataCollector
from mesa.space import SingleGrid
from mesa.time import SimultaneousActivation 

from agent2 import TreeCell

class ForestFire(Model):
    """
        Simple Forest Fire model.

        Attributes:
            height, width: Grid size.
            density: What fraction of grid cells have a tree in them.
    """

    def __init__(self, height=50, width=50, density=0.35):
        """
        Create a new forest fire model.
        
        Args:
            height, width: The size of the grid to model
            density: What fraction of grid cells have a tree in them.
        """

        # Set up model objects
        # SimultaneousActivation is a Mesa object that runs all the agents at the same time. 
        # This is necessary in this model because the next state of each cell depends on the current state of all its neighbors -- before they've changed.
        # This activation method requires that all the agents have a step() and an advance() method. 
        # The step() method computes the next state of the agent, and the advance() method sets the state to the new computed state.
        self.schedule = SimultaneousActivation(self)
        self.grid = SingleGrid(height, width, torus=True)

        # A datacollector is a Mesa object for collecting data about the model.
        # We'll use it to count the number of trees in each condition each step.
        self.datacollector = DataCollector(
            {
                "Aljve": lambda m: self.count_type(m, "Alive"),
                "Dead": lambda m: self.count_type(m, "Dead"),
            }
        )

        # Place a tree in each cell with Prob = density
        # coord_iter is an iterator that returns positions as well as cell contents.
        for contents, (x, y) in self.grid.coord_iter():
            new_tree = TreeCell((x, y), self)
            # Llenar el grid de célculas vivas y muertas aleatoriamente
            if self.random.random() < density:
                # Create a tree
                new_tree.condition = "Alive"

                # Set all trees in the first column on fire.
            else:
                new_tree.condition = "Dead"
                
            self.grid.place_agent(new_tree, (x, y))
            self.schedule.add(new_tree)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """
        Have the scheduler advance each cell by one step
        """
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)


    # staticmethod is a Python decorator that makes a method callable without an instance.
    @staticmethod
    def count_type(model, tree_condition):
        """
        Helper method to count trees in a given condition in a given model.
        """
        count = 0
        for tree in model.schedule.agents:
            if tree.condition == tree_condition:
                count += 1
        return count