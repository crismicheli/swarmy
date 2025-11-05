"""
Custom Agent Behavior Example
----------------------------
Demonstrates how to subclass and override Agent behavior in swarmy.
"""
from swarmy.core.agent import Agent
from swarmy.core.simulation import SwarmSimulation
from swarmy import SimulationConfig

class MyAgent(Agent):
    def step(self, *args, **kwargs):
        """Override: always move upward."""
        self.direction = 1.57  # Point straight up
        super().step(*args, **kwargs)

config = SimulationConfig(num_agents=30)
sim = SwarmSimulation(config)
for i in range(len(sim.agents)):
    sim.agents[i] = MyAgent(**vars(sim.agents[i]))  # Replace with custom agents

for step in range(200):
    sim.step()
    # Add debug/print as needed
