"""
Matplotlib Visualization Renderer
--------------------------------
Static or batch visualization using matplotlib (plots at each timestep).
"""
import matplotlib.pyplot as plt
from swarmy.visualization.renderer_base import RendererBase

class MatplotlibRenderer(RendererBase):
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.fig, self.ax = plt.subplots(figsize=(width/100, height/100))
        plt.ion()
        plt.show()

    def render(self, state):
        self.ax.clear()
        for agent in state['agents']:
            color = 'tab:blue' if not agent['is_scout'] else 'tab:orange'
            self.ax.plot(agent['position'][0], agent['position'][1], 'o', color=color, markersize=4, alpha=0.7)
        for queen in state['queens']:
            self.ax.plot(queen['position'][0], queen['position'][1], 'o', color='gold', markersize=15, alpha=0.6)
        for resource in state['resources']:
            color = {'red':'red','green':'green','blue':'blue'}.get(resource['resource_type'],'gray')
            self.ax.plot(resource['position'][0], resource['position'][1], 'o', color=color, markersize=10, alpha=0.5)
        self.ax.set_xlim(0, self.width)
        self.ax.set_ylim(0, self.height)
        self.ax.set_title('Swarmy: Matplotlib Visualization')
        plt.pause(0.001)
