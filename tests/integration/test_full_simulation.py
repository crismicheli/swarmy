"""
Integration test to run a full simulation and check outcomes.
"""
from swarmy import SwarmSimulation, SimulationConfig
from swarmy.utils import SwarmMetrics

def test_full_simulation_runs():
    config = SimulationConfig(num_agents=10, num_resources=2)
    sim = SwarmSimulation(config)
    metrics = SwarmMetrics()
    for step in range(200):
        sim.step()
        metrics.record(sim.get_state(), step)
    summary = metrics.summary()
    assert summary['final_agents'] > 0
    assert summary['total_collected'] >= 0
