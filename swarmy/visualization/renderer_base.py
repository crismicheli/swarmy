"""
Abstract Renderer Base Class
---------------------------
Defines the interface for visualization modules.
"""
from abc import ABC, abstractmethod

class RendererBase(ABC):
    """
    Abstract base class for all Swarmy visualization renderers.
    """

    @abstractmethod
    def render(self, state):
        """
        Render the current simulation state.
        Args:
            state (dict): Dictionary from sim.get_state()
        """
        pass
