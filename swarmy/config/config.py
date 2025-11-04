"""
Configuration management for Swarmy simulation.
"""
from dataclasses import dataclass, field
from typing import Tuple, List

@dataclass
class SimulationConfig:
    """Configuration parameters for the swarm simulation."""

    # Environment
    width: float = 800.0
    height: float = 600.0
    wrap_boundaries: bool = False  # Toroidal vs bounded

    # Agent parameters
    num_agents: int = 100
    num_scouts: int = 10
    agent_speed_min: float = 1.0
    agent_speed_max: float = 2.0
    agent_radius: float = 3.0
    communication_radius: float = 50.0
    direction_perturbation: float = 0.1  # radians per step
    agent_lifespan_min: int = 5000
    agent_lifespan_max: int = 10000

    # Resource parameters
    num_resources: int = 3
    resource_types: List[str] = field(default_factory=lambda: ['red', 'green', 'blue'])
    resource_capacity_min: int = 50
    resource_capacity_max: int = 100
    resource_radius: float = 10.0
    resource_movement_speed: float = 0.5

    # Queen parameters
    num_queens: int = 1
    queen_radius: float = 15.0
    queen_distance_threshold: float = 1000.0  # Distance for agent to become queen
    queen_creation_cost: dict = field(default_factory=lambda: {'red': 1, 'green': 1, 'blue': 1})
    queen_lifespan_extension_cost: int = 1
    queen_initial_lifespan: int = 10000
    queen_movement_speed: float = 0.3
    agent_creation_probability: float = 0.8
    life_extension_probability: float = 0.2
    scout_creation_probability: float = 0.2

    # Simulation
    random_seed: int = None

    def __post_init__(self):
        """Validate configuration."""
        if self.random_seed is not None:
            import numpy as np
            np.random.seed(self.random_seed)

        assert self.width > 0 and self.height > 0, "Invalid environment dimensions"
        assert self.communication_radius > 0, "Communication radius must be positive"
        assert 0 <= self.agent_creation_probability <= 1, "Probability must be in [0,1]"
        assert 0 <= self.life_extension_probability <= 1, "Probability must be in [0,1]"


@dataclass
class VisualizationConfig:
    """Configuration for visualization."""

    fps: int = 60
    show_communication_links: bool = False
    show_agent_directions: bool = True
    show_counters: bool = False

    # Colors (RGB tuples)
    background_color: Tuple[int, int, int] = (240, 240, 240)
    agent_worker_color: Tuple[int, int, int] = (100, 100, 100)
    agent_scout_color: Tuple[int, int, int] = (150, 150, 150)
    queen_color: Tuple[int, int, int] = (255, 215, 0)
    resource_colors: dict = field(default_factory=lambda: {
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255)
    })
    communication_link_color: Tuple[int, int, int] = (200, 200, 200)
