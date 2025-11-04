# Swarmy: Swarm Intelligence Simulation

A Python package implementing a swarm intelligence simulation where agents use distance-limited communication ("shouts") to collectively gather resources without centralized control.

## Overview

**Swarmy** demonstrates emergent swarm intelligence through simple agent rules:
- Agents are "blind" and move with random perturbations
- They communicate counter values to nearby agents within a radius
- Counter gradients emerge, guiding agents to resources and bases (queens)
- Paths self-organize and optimize over time
- Queens emerge dynamically when agents are isolated
- Resources move and deplete, requiring continuous adaptation

## Features

### Core Simulation (Algorithmic Module)
- **Modular architecture** - Core simulation completely separated from visualization
- **Agent types** - Worker agents (assigned resources) and scout agents (explorers)
- **Dynamic queens** - Queens can emerge from isolated agents
- **Resource management** - Moving resources with depletion and harvesting
- **Counter-based navigation** - Emergent gradient fields for pathfinding
- **Lifecycle management** - Agent aging, queen lifespan, resource consumption

### Key Parameters
- Agent density and communication radius
- Movement speed variation
- Direction perturbation (prevents straight-line movement)
- Queen distance threshold for emergence
- Resource capacity and movement

## Installation

```bash
# Clone or extract the package
cd swarmy

# Install core package
pip install -e .

# Install with visualization support
pip install -e ".[visualization]"

# Install all optional dependencies
pip install -e ".[visualization,analysis,dev]"
```

## Quick Start

### Basic Simulation (No Visualization)

```python
from swarmy import SwarmSimulation, SimulationConfig

# Create configuration
config = SimulationConfig(
    width=800,
    height=600,
    num_agents=50,
    num_scouts=5,
    num_resources=3,
    communication_radius=50
)

# Create and run simulation
sim = SwarmSimulation(config)

for step in range(1000):
    sim.step()

    # Access simulation state
    state = sim.get_state()
    print(f"Step {step}: {len(state['agents'])} agents, "
          f"{len(state['queens'])} queens")
```

### Run Example

```bash
cd examples
python basic_simulation.py
```

## Package Structure

```
swarmy/
├── __init__.py                    # Main package interface
├── core/                          # Core simulation (no visualization)
│   ├── __init__.py
│   ├── agent.py                   # Agent class with counter logic
│   ├── queen.py                   # Queen class for bases
│   ├── resource.py                # Resource class
│   ├── simulation.py              # Main simulation engine
│   └── utils.py                   # Utility functions
├── config/                        # Configuration management
│   ├── __init__.py
│   └── config.py                  # SimulationConfig class
└── visualization/                 # Visualization module (separate)
    ├── __init__.py
    ├── renderer_base.py          # Abstract renderer
    ├── pygame_renderer.py        # Pygame implementation
    └── matplotlib_renderer.py    # Matplotlib implementation

examples/                          # Example scripts
├── basic_simulation.py           # Basic example
├── multi_queen.py                # Multiple queens scenario
└── api_usage.py                  # Comprehensive API usage

tests/                            # Unit tests
├── test_agent.py
├── test_queen.py
├── test_resource.py
└── test_simulation.py
```

## Architecture

### Modular Design

The package follows a strict separation of concerns:

1. **Core Module** (`swarmy.core`)
   - Pure algorithmic implementation
   - No dependencies on visualization libraries
   - Can run headless for batch simulations, analysis, or optimization
   - Clean API: `step()`, `get_state()`, add/remove entities

2. **Configuration Module** (`swarmy.config`)
   - Centralized parameter management
   - `SimulationConfig` for simulation parameters
   - `VisualizationConfig` for rendering options
   - Easy to save/load configurations

3. **Visualization Module** (`swarmy.visualization`)
   - Pluggable renderers (Pygame, Matplotlib, etc.)
   - Completely optional - can be excluded for production use
   - Receives simulation state and renders it
   - No feedback to simulation logic

### Key Classes

#### `SwarmSimulation`
Main simulation engine that orchestrates all components.

**Key Methods:**
- `step()` - Execute one simulation time step
- `get_state()` - Get complete state as dictionary
- `add_agent()`, `add_queen()`, `add_resource()` - Add entities

#### `Agent`
Individual swarm agent with counter-based navigation.

**Key Attributes:**
- `position`, `direction`, `speed`
- `counters` - Dictionary mapping target types to estimated steps
- `current_objective` - Current target
- `carried_resource` - Resource being carried (if any)

**Key Methods:**
- `step()` - Move and update counters
- `collision_with_target()` - Handle target collision
- `receive_message()` - Process communication from other agent

#### `Queen`
Base that receives resources and creates new agents.

**Key Attributes:**
- `position`, `lifespan`
- `inventory` - Resources collected
- `alive` - Whether queen is still alive

**Key Methods:**
- `step()` - Move toward furthest resource
- `receive_resource()` - Accept resource from agent
- `try_create_agent()` - Attempt to spawn new agent
- `try_extend_life()` - Use resources to extend lifespan

#### `Resource`
Collectible resource that moves and depletes.

**Key Attributes:**
- `position`, `resource_type`
- `capacity` - Remaining amount
- `depleted` - Whether fully harvested

**Key Methods:**
- `step()` - Random movement
- `harvest()` - Remove some capacity

## Algorithm Details

### Agent Algorithm (per time step)

1. **Move**: Step forward with random angular perturbation
2. **Increment counters**: All counters increase by 1
3. **Check collisions**:
   - Resource collision → pick up resource, reset counter
   - Queen collision → deliver resource, reset counter
4. **Broadcast**: Shout counter values + communication radius
5. **Listen**: Update counters based on nearby agents' shouts
6. **Navigate**: Turn toward better gradient if objective matches
7. **Age**: Increment age, check for death

### Communication Protocol

- Each agent broadcasts: `counter_value + communication_radius`
- Receiving agent calculates: `new_counter = broadcast_value - comm_radius + distance + 1`
- Update only if new value is better (lower)
- If updated and target is objective, turn toward sender
- Creates emergent gradient field guiding agents to targets

### Queen Behavior

- Moves slowly toward furthest resource
- Receives resources from agents
- With all 3 resource types: can create agent or extend life
- Probabilistic decision between creation and life extension
- Agents far from queens can become new queens

### Path Formation

- Emerges from counter gradient propagation
- Shorter paths dominate (longer paths die off quickly)
- Paths adapt dynamically to moving targets
- Tend toward straightness over time
- Wide fan search when target lost

## Configuration

### Simulation Parameters

```python
config = SimulationConfig(
    # Environment
    width=800.0,
    height=600.0,
    wrap_boundaries=False,  # Toroidal vs bounded

    # Agents
    num_agents=100,
    num_scouts=10,
    agent_speed_min=1.0,
    agent_speed_max=2.0,
    communication_radius=50.0,
    direction_perturbation=0.1,  # radians
    agent_lifespan_min=5000,
    agent_lifespan_max=10000,

    # Resources
    num_resources=3,
    resource_types=['red', 'green', 'blue'],
    resource_capacity_min=50,
    resource_capacity_max=100,
    resource_movement_speed=0.5,

    # Queens
    num_queens=1,
    queen_distance_threshold=1000.0,
    agent_creation_probability=0.8,
    life_extension_probability=0.2,

    # Simulation
    random_seed=42
)
```

## Use Cases

### Research & Analysis
- Study emergent swarm behaviors
- Analyze communication patterns
- Test optimization strategies
- Batch simulations for parameter sweeps

### Education
- Demonstrate swarm intelligence principles
- Visualize emergent behavior
- Interactive exploration of parameters

### Algorithm Development
- Test communication protocols
- Experiment with agent behaviors
- Develop new swarm algorithms

## Performance

- Supports 1000+ agents in real-time
- Efficient spatial lookups for communication
- Optimized NumPy operations
- Headless mode for fast batch simulations

## License

MIT License - See LICENSE file for details

## Citation

If you use this package in academic work, please cite:

```bibtex
@software{swarmy,
  title={Swarmy: A Swarm Intelligence Simulation},
  author={Swarm Intelligence Research},
  year={2025},
  version={1.0.0}
}
```

## Contact

For questions, issues, or suggestions, please open an issue on the repository.
