"""
Multi-queen simulation example.

Demonstrates dynamic queen emergence and competition.
"""

import sys
sys.path.insert(0, '..')

from swarmy import SwarmSimulation, SimulationConfig

def run_multi_queen_simulation():
    """Run simulation that encourages queen emergence."""

    # Configuration favoring queen emergence
    config = SimulationConfig(
        width=1200,
        height=900,
        num_agents=150,
        num_scouts=20,
        num_resources=6,
        num_queens=1,
        communication_radius=40,  # Smaller radius
        queen_distance_threshold=300,  # Lower threshold for emergence
        agent_lifespan_min=8000,
        agent_lifespan_max=15000,
        random_seed=123
    )

    sim = SwarmSimulation(config)

    print("="*60)
    print("Multi-Queen Emergence Simulation")
    print("="*60)
    print("This simulation encourages queen emergence through:")
    print("  - Large environment")
    print("  - Multiple scattered resources")
    print("  - Lower queen distance threshold")
    print("  - Smaller communication radius")
    print("="*60)

    for step in range(2000):
        sim.step()

        if (step + 1) % 200 == 0:
            state = sim.get_state()

            alive_queens = [q for q in state['queens'] if q['alive']]
            alive_agents = sum(1 for a in state['agents'] if a['alive'])

            print(f"\nStep {step+1}:")
            print(f"  Queens: {len(alive_queens)}")
            print(f"  Agents: {alive_agents}")

            for i, queen in enumerate(alive_queens):
                total_resources = sum(queen['inventory'].values())
                print(f"    Queen {i}: health={queen['health_ratio']*100:.0f}%, "
                      f"resources={total_resources}, "
                      f"pos=({queen['position'][0]:.0f}, {queen['position'][1]:.0f})")

    print("\n" + "="*60)
    print("Simulation complete!")

if __name__ == '__main__':
    run_multi_queen_simulation()
