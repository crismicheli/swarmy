"""
Basic simulation example using the Swarmy package.

This example demonstrates the core simulation without visualization,
showing how to run the simulation and access its state.
"""

import sys
sys.path.insert(0, '..')

from swarmy import SwarmSimulation, SimulationConfig
import time

def run_basic_simulation():
    """Run a basic simulation and print statistics."""

    # Create configuration
    config = SimulationConfig(
        width=800,
        height=600,
        num_agents=50,
        num_scouts=5,
        num_resources=3,
        num_queens=1,
        communication_radius=50,
        random_seed=42
    )

    # Create simulation
    sim = SwarmSimulation(config)

    print("="*60)
    print("Swarmy - Basic Simulation")
    print("="*60)
    print(f"Environment: {config.width}x{config.height}")
    print(f"Agents: {config.num_agents} (including {config.num_scouts} scouts)")
    print(f"Resources: {config.num_resources}")
    print(f"Queens: {config.num_queens}")
    print(f"Communication radius: {config.communication_radius}")
    print("="*60)

    # Run simulation for a number of steps
    num_steps = 1000
    print_interval = 100

    start_time = time.time()

    for step in range(num_steps):
        sim.step()

        if (step + 1) % print_interval == 0:
            state = sim.get_state()

            alive_agents = sum(1 for a in state['agents'] if a['alive'])
            alive_queens = sum(1 for q in state['queens'] if q['alive'])
            active_resources = sum(1 for r in state['resources'] if not r['depleted'])

            total_inventory = sum(
                sum(q['inventory'].values()) 
                for q in state['queens'] 
                if q['alive']
            )

            print(f"Step {step+1:4d}: "
                  f"Agents={alive_agents:3d}, "
                  f"Queens={alive_queens:2d}, "
                  f"Resources={active_resources:2d}, "
                  f"Total collected={total_inventory:3d}")

    elapsed_time = time.time() - start_time
    print("="*60)
    print(f"Simulation completed in {elapsed_time:.2f} seconds")
    print(f"Steps per second: {num_steps/elapsed_time:.1f}")
    print("="*60)

    # Print final statistics
    final_state = sim.get_state()
    print("\nFinal Statistics:")
    print(f"  Living agents: {sum(1 for a in final_state['agents'] if a['alive'])}")
    print(f"  Living queens: {sum(1 for q in final_state['queens'] if q['alive'])}")
    print(f"  Active resources: {sum(1 for r in final_state['resources'] if not r['depleted'])}")

    for i, queen in enumerate(final_state['queens']):
        if queen['alive']:
            print(f"  Queen {i} inventory: {queen['inventory']}")
            print(f"  Queen {i} health: {queen['health_ratio']*100:.1f}%")

if __name__ == '__main__':
    run_basic_simulation()
