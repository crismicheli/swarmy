"""
Batch Simulation Example
-----------------------
Run several simulations with different random seeds and aggregate statistics.
"""
from swarmy import SwarmSimulation, SimulationConfig
from swarmy.utils import SwarmMetrics
import numpy as np

n_runs = 10
efficiencies = []
for i in range(n_runs):
    config = SimulationConfig(random_seed=i)
    sim = SwarmSimulation(config)
    metrics = SwarmMetrics()
    for step in range(1000):
        sim.step()
        metrics.record(sim.get_state(), step)
    eff = metrics.get_efficiency()
    efficiencies.append(eff)
    print(f"Run {i+1}: Efficiency={eff:.3f}")

mean_eff = np.mean(efficiencies)
std_eff = np.std(efficiencies)
print(f"
Mean efficiency over {n_runs} runs: {mean_eff:.2f} ± {std_eff:.2f}")
