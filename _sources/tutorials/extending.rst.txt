Extending Swarmy
==============

How to add new agent/queen/resource logic or integrate new visualizations:

.. code-block:: python

    from swarmy.core.agent import Agent
    class CustomAgent(Agent):
        def step(self, *args, **kwargs):
            # Custom behavior
            super().step(*args, **kwargs)

You can also subclass Resource, Queen, or extend SwarmSimulation.
