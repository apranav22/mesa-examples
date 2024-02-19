"""
Sugarscape Constant Growback Model
================================

Replication of the model found in Netlogo:
Li, J. and Wilensky, U. (2009). NetLogo Sugarscape 2 Constant Growback model.
http://ccl.northwestern.edu/netlogo/models/Sugarscape2ConstantGrowback.
Center for Connected Learning and Computer-Based Modeling,
Northwestern University, Evanston, IL.
"""

from pathlib import Path

import mesa

from .agents import SsAgent, Sugar


class SugarscapeScc(mesa.Model):
    """
    Sugarscape 3 SCC
    """

    verbose = True  # Print-monitoring

    def __init__(self, width=50, height=50, initial_population=100):
        """
        Create a new Constant Growback model with the given parameters.

        Args:
            initial_population: Number of population to start with
        """
        super().__init__()

        # Set parameters
        self.width = width
        self.height = height
        self.initial_population = initial_population
        self.schedule = mesa.time.RandomActivationByType(self)
        self.grid = mesa.space.MultiGrid(self.width, self.height, torus=False)
        self.datacollector = mesa.DataCollector(
            {"SsAgent": lambda m: m.schedule.get_type_count(SsAgent)}
        )

        # Create sugar
        import numpy as np

        sugar_distribution = np.genfromtxt(Path(__file__).parent / "sugar-map.txt")
        for _, (x, y) in self.grid.coord_iter():
            max_sugar = sugar_distribution[x, y]
            sugar = Sugar(self.next_id(), (x, y), self, max_sugar)
            self.grid.place_agent(sugar, (x, y))
            self.schedule.add(sugar)

        # Create agent:
        for _ in range(self.initial_population):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            sugar = self.random.randrange(50, 100)
            metabolism = self.random.randrange(2, 4)
            vision = self.random.randrange(1, 6)
            ssa = SsAgent(
                self.next_id(), (x, y), self, False, sugar, metabolism, vision
            )
            self.grid.place_agent(ssa, (x, y))
            self.schedule.add(ssa)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        if self.verbose:
            print([self.schedule.time, self.schedule.get_type_count(SsAgent)])

    def run_model(self, step_count=200):
        if self.verbose:
            print(
                "Initial number Sugarscape Agent: ",
                self.schedule.get_type_count(SsAgent),
            )

        for i in range(step_count):
            self.step()

        if self.verbose:
            print("")
            print(
                "Final number Sugarscape Agent: ",
                self.schedule.get_type_count(SsAgent),
            )