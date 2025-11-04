"""
Queen implementation for Swarmy simulation.
"""
import numpy as np
from typing import Tuple, Dict, Optional
from swarmy.core.utils import distance, angle_between, vector_from_angle

class Queen:
    """
    A queen (base) that receives resources and creates new agents.
    """

    _id_counter = 0

    def __init__(
        self,
        position: Tuple[float, float],
        lifespan: int,
        movement_speed: float,
        creation_cost: Dict[str, int],
        life_extension_cost: int,
        agent_creation_probability: float,
        life_extension_probability: float,
        scout_creation_probability: float
    ):
        """
        Initialize a queen.

        Args:
            position: (x, y) coordinates
            lifespan: Initial lifespan
            movement_speed: Speed of movement toward resources
            creation_cost: Cost in resources to create an agent
            life_extension_cost: Cost to extend lifespan
            agent_creation_probability: Probability of creating agent vs extending life
            life_extension_probability: Probability of extending life
            scout_creation_probability: Probability new agent is scout
        """
        self.id = Queen._id_counter
        Queen._id_counter += 1

        self.position = position
        self.lifespan = lifespan
        self.max_lifespan = lifespan
        self.movement_speed = movement_speed
        self.creation_cost = creation_cost
        self.life_extension_cost = life_extension_cost
        self.agent_creation_probability = agent_creation_probability
        self.life_extension_probability = life_extension_probability
        self.scout_creation_probability = scout_creation_probability

        # Resource inventory
        self.inventory = {rtype: 0 for rtype in creation_cost.keys()}

        self.age = 0
        self.alive = True
        self.agents_created = 0

    def step(self, furthest_resource_position: Optional[Tuple[float, float]],
             env_width: float, env_height: float, wrap: bool = False):
        """
        Update queen state: move toward furthest resource, age, etc.

        Args:
            furthest_resource_position: Position of furthest resource
            env_width: Environment width
            env_height: Environment height
            wrap: Whether to wrap around boundaries
        """
        if not self.alive:
            return

        # Age
        self.age += 1
        self.lifespan -= 1

        if self.lifespan <= 0:
            self.alive = False
            return

        # Move toward furthest resource if it exists
        if furthest_resource_position is not None:
            angle = angle_between(self.position, furthest_resource_position)
            dx, dy = vector_from_angle(angle, self.movement_speed)
            new_x = self.position[0] + dx
            new_y = self.position[1] + dy

            if wrap:
                new_x = new_x % env_width
                new_y = new_y % env_height
            else:
                new_x = np.clip(new_x, 0, env_width)
                new_y = np.clip(new_y, 0, env_height)

            self.position = (new_x, new_y)

    def receive_resource(self, resource_type: str):
        """
        Receive a resource from an agent.

        Args:
            resource_type: Type of resource received
        """
        if resource_type in self.inventory:
            self.inventory[resource_type] += 1

    def can_create_agent(self) -> bool:
        """Check if queen has enough resources to create an agent."""
        return all(self.inventory.get(rtype, 0) >= cost 
                  for rtype, cost in self.creation_cost.items())

    def try_create_agent(self) -> Optional[Dict]:
        """
        Attempt to create a new agent.

        Returns:
            Agent parameters dict if creation successful, None otherwise
        """
        if not self.alive or not self.can_create_agent():
            return None

        # Decide whether to create agent or extend life
        if np.random.random() < self.agent_creation_probability:
            # Create agent
            for rtype, cost in self.creation_cost.items():
                self.inventory[rtype] -= cost

            self.agents_created += 1

            # Determine if scout
            is_scout = np.random.random() < self.scout_creation_probability

            # Determine assigned resource (if not scout)
            assigned_resource = None
            if not is_scout:
                assigned_resource = np.random.choice(list(self.creation_cost.keys()))

            return {
                'position': self.position,
                'is_scout': is_scout,
                'assigned_resource': assigned_resource
            }

        return None

    def try_extend_life(self) -> bool:
        """
        Attempt to extend lifespan using resources.

        Returns:
            True if life extended, False otherwise
        """
        if not self.alive:
            return False

        # Check if we have any resources and decide to extend life
        available_resources = [rtype for rtype, count in self.inventory.items() 
                              if count >= self.life_extension_cost]

        if available_resources and np.random.random() < self.life_extension_probability:
            # Use a random available resource
            resource_type = np.random.choice(available_resources)
            self.inventory[resource_type] -= self.life_extension_cost

            # Extend life
            extension = int(self.max_lifespan * 0.1)  # 10% extension
            self.lifespan += extension

            return True

        return False

    def get_health_ratio(self) -> float:
        """Get health ratio (0 = dead, 1 = full health)."""
        return self.lifespan / self.max_lifespan if self.max_lifespan > 0 else 0.0

    def __repr__(self):
        return f"Queen{self.id} at {self.position}, health={self.get_health_ratio():.2f}, inventory={self.inventory}"
