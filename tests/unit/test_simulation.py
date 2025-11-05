"""
Unit tests for the SwarmSimulation class.
"""
import pytest
from swarmy import SwarmSimulation, SimulationConfig

def test_simulation_initialization():
    config = SimulationConfig(num_agents=5, num_resources=2, num_queens=1)
    sim = SwarmSimulation(config)
    assert len(sim.agents) == 5
    assert len(sim.resources) == 2
    assert len(sim.queens) == 1

def test_simulation_step_changes_state():
    config = SimulationConfig(num_agents=5, num_resources=2, num_queens=1)
    sim = SwarmSimulation(config)
    pre_state = sim.get_state()
    sim.step()
    post_state = sim.get_state()
    assert pre_state != post_state
