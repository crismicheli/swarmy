from swarmy import SwarmSimulation, SimulationConfig
from swarmy.utils import SwarmMetrics
import matplotlib.pyplot as plt

radii = [25, 35, 50, 70, 100]
results = []

for radius in radii:
    config = SimulationConfig(communication_radius=radius)
    sim = SwarmSimulation(config)
    metrics = SwarmMetrics()
    for step in range(1000):
        sim.step()
        metrics.record(sim.get_state(), step)
    results.append(metrics.get_efficiency())

plt.plot(radii, results, marker='o')
plt.xlabel('Communication Radius')
plt.ylabel('Efficiency')
plt.title('Parameter Sweep: Communication Radius')
plt.show()
