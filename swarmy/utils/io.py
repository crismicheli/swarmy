"""
Input/output utilities for saving and loading simulations.
"""
import json
import pickle
from pathlib import Path
from typing import Dict, Any
from swarmy.config.config import SimulationConfig


class ConfigLoader:
    """Load and save simulation configurations."""

    @staticmethod
    def load_json(filepath: str) -> SimulationConfig:
        """
        Load configuration from JSON file.

        Args:
            filepath: Path to JSON config file

        Returns:
            SimulationConfig object
        """
        with open(filepath, 'r') as f:
            data = json.load(f)

        return SimulationConfig(**data)

    @staticmethod
    def save_json(config: SimulationConfig, filepath: str):
        """
        Save configuration to JSON file.

        Args:
            config: SimulationConfig to save
            filepath: Path to save JSON file
        """
        # Convert config to dict
        config_dict = {
            'width': config.width,
            'height': config.height,
            'wrap_boundaries': config.wrap_boundaries,
            'num_agents': config.num_agents,
            'num_scouts': config.num_scouts,
            'agent_speed_min': config.agent_speed_min,
            'agent_speed_max': config.agent_speed_max,
            'agent_radius': config.agent_radius,
            'communication_radius': config.communication_radius,
            'direction_perturbation': config.direction_perturbation,
            'agent_lifespan_min': config.agent_lifespan_min,
            'agent_lifespan_max': config.agent_lifespan_max,
            'num_resources': config.num_resources,
            'resource_types': config.resource_types,
            'resource_capacity_min': config.resource_capacity_min,
            'resource_capacity_max': config.resource_capacity_max,
            'resource_radius': config.resource_radius,
            'resource_movement_speed': config.resource_movement_speed,
            'num_queens': config.num_queens,
            'queen_radius': config.queen_radius,
            'queen_distance_threshold': config.queen_distance_threshold,
            'queen_creation_cost': config.queen_creation_cost,
            'queen_lifespan_extension_cost': config.queen_lifespan_extension_cost,
            'queen_initial_lifespan': config.queen_initial_lifespan,
            'queen_movement_speed': config.queen_movement_speed,
            'agent_creation_probability': config.agent_creation_probability,
            'life_extension_probability': config.life_extension_probability,
            'scout_creation_probability': config.scout_creation_probability,
            'random_seed': config.random_seed,
        }

        # Create directory if needed
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, 'w') as f:
            json.dump(config_dict, f, indent=2)

    @staticmethod
    def load_yaml(filepath: str) -> SimulationConfig:
        """
        Load configuration from YAML file (requires PyYAML).

        Args:
            filepath: Path to YAML config file

        Returns:
            SimulationConfig object
        """
        try:
            import yaml
        except ImportError:
            raise ImportError("PyYAML not installed. Install with: pip install pyyaml")

        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)

        return SimulationConfig(**data)

    @staticmethod
    def save_yaml(config: SimulationConfig, filepath: str):
        """
        Save configuration to YAML file (requires PyYAML).

        Args:
            config: SimulationConfig to save
            filepath: Path to save YAML file
        """
        try:
            import yaml
        except ImportError:
            raise ImportError("PyYAML not installed. Install with: pip install pyyaml")

        config_dict = {
            'width': config.width,
            'height': config.height,
            'wrap_boundaries': config.wrap_boundaries,
            'num_agents': config.num_agents,
            'num_scouts': config.num_scouts,
            'agent_speed_min': config.agent_speed_min,
            'agent_speed_max': config.agent_speed_max,
            'communication_radius': config.communication_radius,
            'num_resources': config.num_resources,
            'resource_types': config.resource_types,
            'num_queens': config.num_queens,
            'random_seed': config.random_seed,
        }

        Path(filepath).parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, 'w') as f:
            yaml.dump(config_dict, f, default_flow_style=False)


class SimulationSnapshot:
    """Save and load simulation state snapshots."""

    @staticmethod
    def save_state(state: Dict[str, Any], filepath: str):
        """
        Save simulation state to file.

        Args:
            state: Simulation state from sim.get_state()
            filepath: Path to save
        """
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, 'wb') as f:
            pickle.dump(state, f)

    @staticmethod
    def load_state(filepath: str) -> Dict[str, Any]:
        """
        Load simulation state from file.

        Args:
            filepath: Path to state file

        Returns:
            Simulation state dict
        """
        with open(filepath, 'rb') as f:
            return pickle.load(f)

    @staticmethod
    def export_json(state: Dict[str, Any], filepath: str):
        """
        Export simulation state to JSON (human-readable).

        Args:
            state: Simulation state
            filepath: Path to save JSON
        """
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)

        # Convert state for JSON (some data types need conversion)
        json_state = {}
        for key, value in state.items():
            if key == 'agents' or key == 'queens' or key == 'resources':
                json_state[key] = value  # Already dict/list compatible
            elif key == 'communications':
                json_state[key] = [list(pair) for pair in value]
            else:
                json_state[key] = value

        with open(filepath, 'w') as f:
            json.dump(json_state, f, indent=2)


class DataExporter:
    """Export simulation data to various formats."""

    @staticmethod
    def export_trajectories(states: list, filepath: str):
        """
        Export agent trajectories to CSV.

        Args:
            states: List of simulation states (from multiple steps)
            filepath: Path to save CSV
        """
        import csv

        Path(filepath).parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['step', 'agent_id', 'x', 'y', 'objective', 'carrying'])

            for state in states:
                step = state['step']
                for agent in state['agents']:
                    if agent['alive']:
                        writer.writerow([
                            step,
                            agent['id'],
                            agent['position'][0],
                            agent['position'][1],
                            agent['current_objective'],
                            agent['carried_resource'],
                        ])

    @staticmethod
    def export_resources(states: list, filepath: str):
        """
        Export resource data to CSV.

        Args:
            states: List of simulation states
            filepath: Path to save CSV
        """
        import csv

        Path(filepath).parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['step', 'resource_id', 'type', 'x', 'y', 'remaining_ratio'])

            for state in states:
                step = state['step']
                for resource in state['resources']:
                    writer.writerow([
                        step,
                        resource['id'],
                        resource['resource_type'],
                        resource['position'][0],
                        resource['position'][1],
                        resource['depletion_ratio'],
                    ])

    @staticmethod
    def export_queens(states: list, filepath: str):
        """
        Export queen/base data to CSV.

        Args:
            states: List of simulation states
            filepath: Path to save CSV
        """
        import csv

        Path(filepath).parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['step', 'queen_id', 'x', 'y', 'health', 'red', 'green', 'blue'])

            for state in states:
                step = state['step']
                for queen in state['queens']:
                    if queen['alive']:
                        writer.writerow([
                            step,
                            queen['id'],
                            queen['position'][0],
                            queen['position'][1],
                            queen['health_ratio'],
                            queen['inventory'].get('red', 0),
                            queen['inventory'].get('green', 0),
                            queen['inventory'].get('blue', 0),
                        ])


# Convenience functions

def load_config(filepath: str) -> SimulationConfig:
    """Quick load config from JSON or YAML."""
    if filepath.endswith('.json'):
        return ConfigLoader.load_json(filepath)
    elif filepath.endswith('.yaml') or filepath.endswith('.yml'):
        return ConfigLoader.load_yaml(filepath)
    else:
        raise ValueError("Unsupported format. Use .json or .yaml")


def save_config(config: SimulationConfig, filepath: str):
    """Quick save config to JSON or YAML."""
    if filepath.endswith('.json'):
        ConfigLoader.save_json(config, filepath)
    elif filepath.endswith('.yaml') or filepath.endswith('.yml'):
        ConfigLoader.save_yaml(config, filepath)
    else:
        raise ValueError("Unsupported format. Use .json or .yaml")
