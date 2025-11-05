Quickstart
==========

Get started with Swarmy in minutes:

.. code-block:: python

    from swarmy import SwarmSimulation, SimulationConfig

    config = SimulationConfig(num_agents=100, communication_radius=50)
    sim = SwarmSimulation(config)
    for step in range(100):
        sim.step()
        print(sim.get_state())

For detailed tutorials see :doc:`tutorials/basic_usage` and :doc:`tutorials/custom_scenarios`.
