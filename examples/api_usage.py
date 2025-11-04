"""
Comprehensive API usage example.

Demonstrates how to use the package programmatically for custom scenarios.
"""

import sys
sys.path.insert(0, '..')

from swarmy import (
    SwarmSimulation, SimulationConfig,
    Agent, Queen, Resource
)
import numpy as np

def custom_simulation():
    """Build a custom simulation using the API."""

    print("Creating custom simulation...")

    # Start with minimal configuration
    config = SimulationConfig(
        width=600,
        height=400,
        num_agents=0,  # We'll add manually
        num_scouts=0,
        num_resources=0,
        num_queens=0,
        communication_radius=60,
        random_seed=999
    )

    sim = SwarmSimulation(config)

    # Add custom queen
    print("Adding custom queen at center...")
    queen = sim.add_queen(
        position=(300, 200),
        lifespan=5000,
        movement_speed=0.2,
        creation_cost={'red': 1, 'green': 1, 'blue': 1},
        life_extension_cost=1,
        agent_creation_probability=0.9,
        life_extension_probability=0.1,
        scout_creation_probability=0.15
    )

    # Add resources in a circle around queen
    print("Adding resources in circular pattern...")
    num_resources = 6
    radius = 200
    for i in range(num_resources):
        angle = 2 * np.pi * i / num_resources
        x = 300 + radius * np.cos(angle)
        y = 200 + radius * np.sin(angle)

        rtype = config.resource_types[i % len(config.resource_types)]

        sim.add_resource(
            position=(x, y),
            resource_type=rtype,
            capacity=80,
            movement_speed=0.3
        )

    # Add initial agents near queen
    print("Adding initial swarm...")
    for i in range(30):
        # Random position near queen
        angle = np.random.uniform(0, 2 * np.pi)
        dist = np.random.uniform(10, 50)
        x = 300 + dist * np.cos(angle)
        y = 200 + dist * np.sin(angle)

        sim.add_agent(
            position=(x, y),
            speed=np.random.uniform(1.0, 2.0),
            communication_radius=60,
            direction_perturbation=0.12,
            lifespan=np.random.randint(5000, 10000),
            resource_types=config.resource_types,
            is_scout=(i < 5),  # First 5 are scouts
            assigned_resource=config.resource_types[i % 3] if i >= 5 else None
        )

    print("Running simulation...")
    print("="*60)

    # Run and monitor
    for step in range(500):
        sim.step()

        if (step + 1) % 100 == 0:
            state = sim.get_state()

            # Calculate statistics
            total_collected = sum(
                sum(q['inventory'].values()) 
                for q in state['queens'] if q['alive']
            )

            resources_by_type = {'red': 0, 'green': 0, 'blue': 0}
            for q in state['queens']:
                if q['alive']:
                    for rtype, count in q['inventory'].items():
                        resources_by_type[rtype] += count

            print(f"Step {step+1}:")
            print(f"  Agents: {sum(1 for a in state['agents'] if a['alive'])}")
            print(f"  Resources collected: {total_collected}")
            print(f"    Red: {resources_by_type['red']}, "
                  f"Green: {resources_by_type['green']}, "
                  f"Blue: {resources_by_type['blue']}")
            print(f"  Communications: {len(state['communications'])}")

    print("="*60)
    print("Custom simulation complete!")

    # Access final state
    final_state = sim.get_state()
    print(f"\nFinal state contains:")
    print(f"  {len(final_state['agents'])} agents")
    print(f"  {len(final_state['queens'])} queens")
    print(f"  {len(final_state['resources'])} resources")

if __name__ == '__main__':
    custom_simulation()
