# Utility Modules

Swarmy provides powerful utility modules for spatial indexing, performance analysis, and data management.

## Overview

| Module | Purpose | Key Features |
|--------|---------|--------------|
| **Spatial Indexing** | Fast neighbor lookups | Grid cells, Quadtrees, O(1) queries |
| **Metrics** | Performance tracking | Efficiency, cohesion, growth rate |
| **I/O Utilities** | Save/load data | JSON, YAML, CSV export |

---

## Table of Contents

1. [Spatial Indexing](#spatial-indexing)
2. [Metrics Tracking](#metrics-tracking)
3. [I/O Utilities](#io-utilities)
4. [Complete Example](#complete-example)

---

## Spatial Indexing

### Overview

Swarmy provides two spatial indexing structures for efficiently finding nearby agents:

- **SpatialGrid**: Regular grid partitioning (fastest for uniform distributions)
- **Quadtree**: Hierarchical tree structure (best for sparse distributions)

### SpatialGrid

Fast neighbor queries using a regular grid.

**Basic Usage:**

```python
from swarmy.utils import SpatialGrid

# Create a spatial grid
grid = SpatialGrid(width=800, height=600, cell_size=50)

# Add agents at positions
for agent in agents:
    grid.add_agent(agent.id, agent.position[0], agent.position[1])

# Find all agents within radius
nearby_agents = grid.get_nearby_agents(x=100, y=100, radius=50)
print(f"Found {len(nearby_agents)} nearby agents")

# Update agent positions
grid.remove_agent(agent.id, old_x, old_y)
grid.add_agent(agent.id, new_x, new_y)

# Rebuild entire grid (useful after many position changes)
grid.rebuild(agents)
```

**Parameters:**

- `width`, `height`: Environment dimensions
- `cell_size`: Size of each grid cell (smaller = finer granularity)
- `radius`: Search radius (in same units as positions)

**Performance:**

- Adding agent: O(1)
- Finding nearby: O(1) average case
- Rebuilding: O(n) where n = number of agents

### Quadtree

Hierarchical spatial indexing for sparse agent distributions.

**Basic Usage:**

```python
from swarmy.utils import Quadtree

# Create quadtree (x, y, width, height, max_depth)
tree = Quadtree(x=0, y=0, width=800, height=600, max_depth=8)

# Insert agents
for agent in agents:
    tree.insert(agent.id, agent.position[0], agent.position[1])

# Query range (returns set of agent IDs)
nearby = tree.query_range(qx=100, qy=100, radius=50)
```

**Advantages over SpatialGrid:**

- Better for non-uniform agent distributions
- Automatic subdivision when regions become crowded
- Memory-efficient for sparse environments

---

## Metrics Tracking

### Overview

Track swarm performance metrics over time, including efficiency, cohesion, and growth rates.

### Basic Usage

```python
from swarmy import SwarmSimulation, SimulationConfig
from swarmy.utils import SwarmMetrics

# Create simulation
config = SimulationConfig(num_agents=100, communication_radius=50)
sim = SwarmSimulation(config)

# Create metrics tracker
metrics = SwarmMetrics()

# Run simulation and track metrics
for step in range(1000):
    sim.step()
    state = sim.get_state()
    metrics.record(state, step)
    
    # Print progress
    if step % 100 == 0:
        print(f"Step {step}: efficiency={metrics.get_efficiency():.2f}")
```

### Recorded Metrics

Each step records:

- **num_agents**: Number of living agents
- **num_queens**: Number of living queens
- **num_resources**: Number of non-depleted resources
- **total_collected**: Total resources collected by all queens
- **avg_agent_age**: Average age ratio of agents
- **swarm_diameter**: Maximum distance between any two agents
- **agent_scatter**: Standard deviation of agent positions
- **communication_events**: Number of agent-to-agent communications

### Available Methods

```python
# Get summary statistics
summary = metrics.summary()
print(summary)
# Output: {
#   'final_agents': 45,
#   'final_queens': 2,
#   'total_collected': 156,
#   'efficiency': 3.47,
#   'cohesion': 0.82,
#   'growth_rate': -10.5,
#   'collection_rate': 15
# }

# Get derived metrics
efficiency = metrics.get_efficiency()      # Resources per agent-step
cohesion = metrics.get_cohesion()          # 0=scattered, 1=cohesive
growth_rate = metrics.get_growth_rate()    # Agents per 100 steps
collection_rate = metrics.get_collection_rate()  # Resources per 100 steps

# Export to CSV
metrics.export_csv('simulation_metrics.csv')

# Plot metrics (requires matplotlib)
metrics.plot_metrics('metrics_plot.png')

# Access raw history
print(metrics.history['total_collected'])
print(metrics.history['num_agents'])
```

### Interpretation

- **Efficiency**: Higher is better (more resources per agent effort)
- **Cohesion**: 0-1 scale, higher means agents stay close together
- **Growth Rate**: Positive = growing, negative = shrinking population
- **Collection Rate**: Resources per 100 steps

### Example: Optimization

```python
# Track metrics for different communication radii
for radius in [30, 50, 70, 90]:
    config = SimulationConfig(communication_radius=radius)
    sim = SwarmSimulation(config)
    metrics = SwarmMetrics()
    
    for step in range(1000):
        sim.step()
        metrics.record(sim.get_state(), step)
    
    summary = metrics.summary()
    print(f"Radius={radius}: Efficiency={summary['efficiency']:.2f}")
```

---

## I/O Utilities

### Overview

Save and load configurations, export simulation data to various formats.

### Configuration Management

**Save Configuration:**

```python
from swarmy.utils import save_config
from swarmy import SimulationConfig

config = SimulationConfig(
    width=800,
    height=600,
    num_agents=100,
    communication_radius=50
)

# Save to JSON
save_config(config, 'my_simulation.json')

# Save to YAML
save_config(config, 'my_simulation.yaml')
```

**Load Configuration:**

```python
from swarmy.utils import load_config

# Load from JSON
config = load_config('my_simulation.json')

# Load from YAML
config = load_config('my_simulation.yaml')

# Use loaded config
sim = SwarmSimulation(config)
```

### Export Simulation Data

**Export Metrics:**

```python
metrics.export_csv('metrics.csv')
```

Output columns: `step, num_agents, num_queens, num_resources, total_collected, ...`

**Export Trajectories:**

```python
from swarmy.utils import DataExporter

# Collect states from simulation
states = []
for step in range(1000):
    sim.step()
    states.append(sim.get_state())

# Export agent trajectories
DataExporter.export_trajectories(states, 'trajectories.csv')
```

Output columns: `step, agent_id, x, y, objective, carrying`

**Export Queen Data:**

```python
# Export queen/base positions and inventories
DataExporter.export_queens(states, 'queens.csv')
```

Output columns: `step, queen_id, x, y, health, red, green, blue`

**Export Resource Data:**

```python
# Export resource positions and depletion
DataExporter.export_resources(states, 'resources.csv')
```

Output columns: `step, resource_id, type, x, y, remaining_ratio`

---

## Complete Example

**Full workflow combining all utilities:**

```python
from swarmy import SwarmSimulation, SimulationConfig
from swarmy.utils import (
    SpatialGrid,
    SwarmMetrics,
    DataExporter,
    save_config,
    load_config
)

# ============ SETUP ============

# Load or create configuration
try:
    config = load_config('config.json')
except FileNotFoundError:
    config = SimulationConfig(
        width=800,
        height=600,
        num_agents=100,
        num_scouts=10,
        communication_radius=50,
        random_seed=42
    )
    save_config(config, 'config.json')

# ============ SIMULATION ============

# Create simulation and utilities
sim = SwarmSimulation(config)
metrics = SwarmMetrics()
states = []

# Optional: spatial indexing for performance optimization
grid = SpatialGrid(width=config.width, height=config.height, cell_size=50)

print(f"Running simulation for 1000 steps...")
print(f"Agents: {config.num_agents}, Resources: {config.num_resources}")

# Run simulation
for step in range(1000):
    sim.step()
    state = sim.get_state()
    
    # Track metrics and states
    metrics.record(state, step)
    states.append(state)
    
    # Update spatial grid (optional)
    grid.rebuild([a for a in sim.agents])
    
    # Print progress
    if (step + 1) % 100 == 0:
        summary = metrics.summary()
        efficiency = metrics.get_efficiency()
        print(f"Step {step+1}: "
              f"Agents={summary['final_agents']}, "
              f"Collected={summary['total_collected']}, "
              f"Efficiency={efficiency:.2f}")

# ============ ANALYSIS ============

# Get final summary
final_summary = metrics.summary()
print("\n" + "="*50)
print("FINAL RESULTS")
print("="*50)
for key, value in final_summary.items():
    print(f"{key:20s}: {value}")

# ============ EXPORT ============

# Export all data
print("\nExporting data...")
metrics.export_csv('metrics.csv')
metrics.plot_metrics('metrics_plot.png')

DataExporter.export_trajectories(states, 'trajectories.csv')
DataExporter.export_queens(states, 'queens.csv')
DataExporter.export_resources(states, 'resources.csv')

print("✅ Export complete!")
print("   - metrics.csv: Simulation statistics over time")
print("   - metrics_plot.png: Visual analysis")
print("   - trajectories.csv: Agent positions and movements")
print("   - queens.csv: Queen positions and inventories")
print("   - resources.csv: Resource positions and depletion")
```

**Output files generated:**

- `metrics.csv` - Time series of swarm metrics
- `metrics_plot.png` - Visualization of metrics
- `trajectories.csv` - Agent movement data
- `queens.csv` - Queen/base status
- `resources.csv` - Resource status

---

## Performance Tips

### Spatial Indexing

```python
# ✅ Good: Rebuild periodically for large position changes
grid.rebuild(agents)  # Every 100 steps

# ❌ Avoid: Adding/removing individual agents constantly
# Instead: collect changes, rebuild once per step
```

### Metrics

```python
# ✅ Good: Record every step
metrics.record(state, step)

# ✅ Good: Export after simulation
metrics.export_csv('results.csv')

# ❌ Avoid: Recording too frequently (memory intensive)
# If needed: record every nth step instead
if step % 10 == 0:
    metrics.record(state, step)
```

### Data Export

```python
# ✅ Good: Export after collecting states
states = [state1, state2, ...]
DataExporter.export_trajectories(states, 'file.csv')

# ❌ Avoid: Exporting each state individually (slow)
```

---

## See Also

- [Core Simulation](../README.md#architecture) - Main SwarmSimulation class
- [Configuration](../README.md#configuration) - SimulationConfig options
- [Examples](../examples/) - Complete working examples

---

## API Reference

### `swarmy.utils.SpatialGrid`

```python
class SpatialGrid:
    def __init__(self, width: float, height: float, cell_size: float)
    def add_agent(self, agent_id: int, x: float, y: float)
    def remove_agent(self, agent_id: int, x: float, y: float)
    def get_nearby_agents(self, x: float, y: float, radius: float) -> Set[int]
    def rebuild(self, agents: List[Agent])
    def clear(self)
```

### `swarmy.utils.SwarmMetrics`

```python
class SwarmMetrics:
    def record(self, state: Dict, step: int)
    def get_efficiency(self) -> float
    def get_cohesion(self) -> float
    def get_growth_rate(self) -> float
    def get_collection_rate(self) -> float
    def summary(self) -> Dict
    def export_csv(self, filename: str)
    def plot_metrics(self, save_path: str = None)
```

### `swarmy.utils.ConfigLoader`

```python
class ConfigLoader:
    @staticmethod
    def load_json(filepath: str) -> SimulationConfig
    @staticmethod
    def save_json(config: SimulationConfig, filepath: str)
    @staticmethod
    def load_yaml(filepath: str) -> SimulationConfig
    @staticmethod
    def save_yaml(config: SimulationConfig, filepath: str)
```

### `swarmy.utils.DataExporter`

```python
class DataExporter:
    @staticmethod
    def export_trajectories(states: list, filepath: str)
    @staticmethod
    def export_resources(states: list, filepath: str)
    @staticmethod
    def export_queens(states: list, filepath: str)
```

---

## Questions?

For more information, see the [main README](../README.md) or [examples](../examples/).
