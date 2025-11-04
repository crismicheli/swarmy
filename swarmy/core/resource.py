"""
Resource implementation for Swarmy simulation.
"""
import numpy as np
from typing import Tuple
from swarmy.core.utils import perturb_angle, vector_from_angle

class Resource:
    """
    A resource that agents can collect and deliver to queens.
    """

    _id_counter = 0

    def __init__(
        self,
        position: Tuple[float, float],
        resource_type: str,
        capacity: int,
        movement_speed: float = 0.5
    ):
        """
        Initialize a resource.

        Args:
            position: (x, y) coordinates
            resource_type: Type identifier ('red', 'green', 'blue', etc.)
            capacity: Total amount of resource available
            movement_speed: Speed at which resource moves
        """
        self.id = Resource._id_counter
        Resource._id_counter += 1

        self.position = position
        self.resource_type = resource_type
        self.capacity = capacity
        self.initial_capacity = capacity
        self.movement_speed = movement_speed
        self.direction = np.random.uniform(0, 2 * np.pi)
        self.depleted = False

    def step(self, env_width: float, env_height: float, wrap: bool = False):
        """
        Move the resource (resources drift around).

        Args:
            env_width: Environment width
            env_height: Environment height
            wrap: Whether to wrap around boundaries
        """
        if self.depleted:
            return

        # Random walk with occasional direction changes
        if np.random.random() < 0.05:  # 5% chance to change direction
            self.direction = perturb_angle(self.direction, np.pi / 4)

        # Move
        dx, dy = vector_from_angle(self.direction, self.movement_speed)
        new_x = self.position[0] + dx
        new_y = self.position[1] + dy

        # Handle boundaries
        if wrap:
            new_x = new_x % env_width
            new_y = new_y % env_height
        else:
            # Bounce off walls
            if new_x < 0 or new_x > env_width:
                self.direction = np.pi - self.direction
                new_x = np.clip(new_x, 0, env_width)
            if new_y < 0 or new_y > env_height:
                self.direction = -self.direction
                new_y = np.clip(new_y, 0, env_height)

        self.position = (new_x, new_y)

    def harvest(self, amount: int = 1) -> bool:
        """
        Harvest some amount from this resource.

        Args:
            amount: Amount to harvest

        Returns:
            True if harvest successful, False if depleted
        """
        if self.depleted:
            return False

        self.capacity -= amount
        if self.capacity <= 0:
            self.depleted = True
            return False

        return True

    def get_depletion_ratio(self) -> float:
        """Get ratio of remaining capacity (0 = depleted, 1 = full)."""
        return self.capacity / self.initial_capacity if self.initial_capacity > 0 else 0.0

    def __repr__(self):
        return f"Resource{self.id}({self.resource_type}) at {self.position}, capacity={self.capacity}"
