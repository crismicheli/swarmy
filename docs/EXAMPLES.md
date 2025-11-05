# Advanced Example Scripts

The `examples/` directory contains advanced scripts illustrating how to use, analyze, and extend the `swarmy` package.

| Script                    | Purpose                                      | Key Features                    |
|---------------------------|----------------------------------------------|----------------------------------|
| parameter_sweep.py        | Test parameter effects on swarm efficiency   | Parameter sweep, matplotlib      |
| batch_simulation.py       | Run multiple seeds, aggregate results        | Batch stats, numpy              |
| optimization_study.py     | Find optimal parameter settings              | Grid search, performance        |
| custom_behavior.py        | Add new agent logic by subclassing           | OOP extension                   |
| visualization_demo.py     | Visualize simulation (if available)          | Pygame integration              |

---

## parameter_sweep.py

Sweeps over different `communication_radius` values and plots their effects on efficiency. Useful for identifying best parameter regions.

## batch_simulation.py

Runs multiple simulations with different seeds and prints average and standard deviation of efficiency. Useful for measuring reproducibility and natural variance in your algorithms.

## optimization_study.py

Grid search exploring multiple combinations of communication radius and agent speeds. Designed to find configurations that maximize resource collection efficiency.

## custom_behavior.py

Demonstrates how you can subclass `Agent` and override the `step` method to customize agent movement, perception, or communication.

## visualization_demo.py

If `swarmy.visualization` is installed, this launches a real-time visualization using Pygame. Adapts core simulation state to the renderer.

---

**You can run any script with:**

```bash
python examples/parameter_sweep.py
python examples/batch_simulation.py
python examples/optimization_study.py
python examples/custom_behavior.py
python examples/visualization_demo.py
```

Check the top of each script for dependencies, and install with pip (`matplotlib`, `numpy`, `pygame` as needed).

For more details, see [UTILS.md](UTILS.md) for how to leverage metrics, export data, and extend core components.
