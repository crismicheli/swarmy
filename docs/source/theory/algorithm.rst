Algorithm Overview
=================

Swarmy uses a hybrid shortest-path / sooting system:

- Agents broadcast counters of distance to targets
- Gradients form guiding other agents via local information
- Emergent paths self-correct and adapt
- Communication is limited by radius (no global view)
