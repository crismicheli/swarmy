"""
Swarmy: A Swarm Intelligence Simulation Package

This package implements a swarm intelligence simulation where agents communicate
through distance-limited broadcasts to collectively solve resource gathering tasks.
"""

__version__ = '1.0.0'
__author__ = 'Swarm Intelligence Research'

from swarmy.config.config import SimulationConfig, VisualizationConfig
from swarmy.core.simulation import SwarmSimulation
from swarmy.core.agent import Agent
from swarmy.core.queen import Queen
from swarmy.core.resource import Resource

__all__ = [
    'SimulationConfig',
    'VisualizationConfig',
    'SwarmSimulation',
    'Agent',
    'Queen',
    'Resource'
]
