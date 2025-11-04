"""
Metrics and performance analysis tools for swarm simulations.
"""
import numpy as np
from typing import Dict, List, Tuple
from swarmy.core.utils import distance


class SwarmMetrics:
    """
    Calculate and track metrics about swarm behavior and performance.
    """

    def __init__(self):
        """Initialize metrics tracker."""
        self.history = {
            'step': [],
            'num_agents': [],
            'num_queens': [],
            'num_resources': [],
            'total_collected': [],
            'avg_agent_age': [],
            'swarm_diameter': [],
            'agent_scatter': [],
            'communication_events': [],
        }

    def record(self, state: Dict, step: int):
        """
        Record metrics for a simulation state.

        Args:
            state: Simulation state dict from sim.get_state()
            step: Current simulation step
        """
        self.history['step'].append(step)

        # Count entities
        agents = [a for a in state['agents'] if a['alive']]
        queens = [q for q in state['queens'] if q['alive']]
        resources = [r for r in state['resources'] if not r['depleted']]

        self.history['num_agents'].append(len(agents))
        self.history['num_queens'].append(len(queens))
        self.history['num_resources'].append(len(resources))

        # Total resources collected
        total = sum(sum(q['inventory'].values()) for q in queens)
        self.history['total_collected'].append(total)

        # Average agent age
        if agents:
            avg_age = np.mean([a['age_ratio'] for a in agents])
        else:
            avg_age = 0.0
        self.history['avg_agent_age'].append(avg_age)

        # Swarm diameter (max distance between any two agents)
        if len(agents) > 1:
            positions = [a['position'] for a in agents]
            max_dist = 0
            for i in range(len(positions)):
                for j in range(i + 1, len(positions)):
                    d = distance(positions[i], positions[j])
                    max_dist = max(max_dist, d)
            self.history['swarm_diameter'].append(max_dist)
        else:
            self.history['swarm_diameter'].append(0.0)

        # Agent scatter (standard deviation of positions)
        if agents:
            xs = [a['position'][0] for a in agents]
            ys = [a['position'][1] for a in agents]
            scatter = np.sqrt(np.std(xs) ** 2 + np.std(ys) ** 2)
        else:
            scatter = 0.0
        self.history['agent_scatter'].append(scatter)

        # Communication events
        self.history['communication_events'].append(len(state['communications']))

    def get_efficiency(self) -> float:
        """
        Calculate efficiency: resources collected / total agent-steps.

        Returns:
            Efficiency metric (higher is better)
        """
        if not self.history['total_collected'] or len(self.history['num_agents']) == 0:
            return 0.0

        total_collected = self.history['total_collected'][-1]
        total_agent_steps = sum(self.history['num_agents'])

        if total_agent_steps == 0:
            return 0.0

        return total_collected / total_agent_steps

    def get_cohesion(self) -> float:
        """
        Calculate cohesion: inverse of average scatter.

        Returns:
            Cohesion metric (higher = more cohesive)
        """
        if not self.history['agent_scatter'] or max(self.history['agent_scatter']) == 0:
            return 0.0

        avg_scatter = np.mean(self.history['agent_scatter'][-100:])  # Last 100 steps
        return 1.0 / (1.0 + avg_scatter)

    def get_growth_rate(self) -> float:
        """
        Calculate population growth rate.

        Returns:
            Growth rate (agents per 100 steps)
        """
        if len(self.history['num_agents']) < 100:
            return 0.0

        current = self.history['num_agents'][-1]
        past = self.history['num_agents'][-100]

        if past == 0:
            return 0.0

        return (current - past) / past * 100

    def get_collection_rate(self) -> float:
        """
        Calculate resource collection rate.

        Returns:
            Resources per 100 steps
        """
        if len(self.history['total_collected']) < 100:
            return 0.0

        current = self.history['total_collected'][-1]
        past = self.history['total_collected'][-100]

        return current - past

    def summary(self) -> Dict:
        """
        Get summary of all metrics.

        Returns:
            Dictionary with summary statistics
        """
        if not self.history['step']:
            return {}

        return {
            'final_step': self.history['step'][-1],
            'final_agents': self.history['num_agents'][-1],
            'final_queens': self.history['num_queens'][-1],
            'total_collected': self.history['total_collected'][-1],
            'avg_scatter': np.mean(self.history['agent_scatter'][-100:]) if len(self.history['agent_scatter']) > 0 else 0,
            'efficiency': self.get_efficiency(),
            'cohesion': self.get_cohesion(),
            'growth_rate': self.get_growth_rate(),
            'collection_rate': self.get_collection_rate(),
        }

    def export_csv(self, filename: str):
        """
        Export metrics history to CSV file.

        Args:
            filename: Output CSV filename
        """
        import csv

        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)

            # Write header
            writer.writerow(self.history.keys())

            # Write data rows
            for i in range(len(self.history['step'])):
                row = [self.history[key][i] for key in self.history.keys()]
                writer.writerow(row)

    def plot_metrics(self, save_path: str = None):
        """
        Plot metrics over time (requires matplotlib).

        Args:
            save_path: Optional path to save plot
        """
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            print("matplotlib not installed. Install with: pip install matplotlib")
            return

        fig, axes = plt.subplots(2, 2, figsize=(12, 8))

        steps = self.history['step']

        # Plot 1: Population
        axes[0, 0].plot(steps, self.history['num_agents'], label='Agents')
        axes[0, 0].plot(steps, self.history['num_queens'], label='Queens')
        axes[0, 0].set_xlabel('Step')
        axes[0, 0].set_ylabel('Count')
        axes[0, 0].set_title('Population Over Time')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)

        # Plot 2: Resources Collected
        axes[0, 1].plot(steps, self.history['total_collected'], color='green')
        axes[0, 1].set_xlabel('Step')
        axes[0, 1].set_ylabel('Total Collected')
        axes[0, 1].set_title('Resource Collection Over Time')
        axes[0, 1].grid(True, alpha=0.3)

        # Plot 3: Swarm Diameter
        axes[1, 0].plot(steps, self.history['swarm_diameter'], color='red')
        axes[1, 0].set_xlabel('Step')
        axes[1, 0].set_ylabel('Diameter')
        axes[1, 0].set_title('Swarm Diameter Over Time')
        axes[1, 0].grid(True, alpha=0.3)

        # Plot 4: Communication Events
        axes[1, 1].plot(steps, self.history['communication_events'], color='blue')
        axes[1, 1].set_xlabel('Step')
        axes[1, 1].set_ylabel('Events')
        axes[1, 1].set_title('Communication Events Over Time')
        axes[1, 1].grid(True, alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=150)
        else:
            plt.show()
