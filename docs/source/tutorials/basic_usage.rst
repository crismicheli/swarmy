Basic Usage Tutorial
===================

This tutorial walks through running your first simulation.

1. Import required modules

   .. code-block:: python

      from swarmy import SwarmSimulation, SimulationConfig

2. Configure your simulation

   .. code-block:: python

      config = SimulationConfig(num_agents=20, communication_radius=40)

3. Initialize and run

   .. code-block:: python

      sim = SwarmSimulation(config)
      for step in range(200):
          sim.step()
          state = sim.get_state()
          print(f"Step {step}: agents={len(state['agents'])}")
