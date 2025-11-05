"""
Visualization Demo Example
-------------------------
Shows how to visualize simulations if visualization module is available.
"""
try:
    from swarmy.visualization.pygame_renderer import PygameRenderer
except ImportError:
    print("Pygame renderer not available. Skipping.")
    exit()

from swarmy import SwarmSimulation, SimulationConfig

config = SimulationConfig(num_agents=50)
sim = SwarmSimulation(config)
renderer = PygameRenderer()

for step in range(1000):
    sim.step()
    renderer.render(sim.get_state())
    if step % 100 == 0:
        print(f"Step {step}")
