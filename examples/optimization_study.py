"""
Optimization Study Example
-------------------------
Grid search: find best communication radius and agent_speed for efficiency.
"""
from swarmy.utils import SwarmMetrics
from swarmy import SwarmSimulation, SimulationConfig
import numpy as np

best_params = None
best_eff = -float('inf')
for radius in [20, 50, 100]:
    for speed in [1, 2, 3]:
        config = SimulationConfig(communication_radius=radius, agent_speed_min=speed, agent_speed_max=speed+0.5)
        sim = SwarmSimulation(config)
        metrics = SwarmMetrics()
        for step in range(1000):
            sim.step()
            metrics.record(sim.get_state(), step)
        eff = metrics.get_efficiency()
        print(f"Radius={radius}, Speed={speed}: Efficiency={eff:.3f}")
        if eff > best_eff:
            best_eff = eff
            best_params = (radius, speed)
print("
Best param set: radius=%s, speed=%s, eff=%.3f" % (*best_params, best_eff))
