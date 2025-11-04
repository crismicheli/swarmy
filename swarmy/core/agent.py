"""
Agent implementation for Swarmy simulation.
"""
import numpy as np
from typing import Tuple, Dict, Optional
from swarmy.core.utils import (
    distance, angle_between, perturb_angle, 
    vector_from_angle, normalize_angle
)

class Agent:
    """
    An agent in the swarm that communicates via 'shouts' and navigates
    using counter gradients.
    """

    _id_counter = 0

    def __init__(
        self,
        position: Tuple[float, float],
        speed: float,
        communication_radius: float,
        direction_perturbation: float,
        lifespan: int,
        resource_types: list,
        is_scout: bool = False,
        assigned_resource: Optional[str] = None
    ):
        """
        Initialize an agent.

        Args:
            position: (x, y) coordinates
            speed: Movement speed per step
            communication_radius: Maximum distance for communication
            direction_perturbation: Maximum angular perturbation per step (radians)
            lifespan: Total lifetime in steps
            resource_types: List of all resource type identifiers
            is_scout: Whether this is a scout agent
            assigned_resource: Resource type this agent should collect (if not scout)
        """
        self.id = Agent._id_counter
        Agent._id_counter += 1

        self.position = position
        self.speed = speed
        self.communication_radius = communication_radius
        self.direction_perturbation = direction_perturbation
        self.is_scout = is_scout
        self.assigned_resource = assigned_resource

        # Direction (angle in radians)
        self.direction = np.random.uniform(0, 2 * np.pi)

        # Counters: estimated steps to each target type
        # Keys: 'queen', 'red', 'green', 'blue', etc.
        self.counters = {'queen': np.random.randint(100, 500)}
        for rtype in resource_types:
            self.counters[rtype] = np.random.randint(100, 500)

        # Current objective
        if is_scout:
            self.current_objective = None  # Scouts roam
        else:
            self.current_objective = assigned_resource if assigned_resource else 'queen'

        # State
        self.carried_resource = None
        self.age = 0
        self.max_age = lifespan
        self.alive = True

    def step(self, env_width: float, env_height: float, wrap: bool = False):
        """
        Take one simulation step: move and increment counters.

        Args:
            env_width: Environment width
            env_height: Environment height
            wrap: Whether to wrap around boundaries
        """
        if not self.alive:
            return

        # Increment age
        self.age += 1
        if self.age >= self.max_age:
            self.alive = False
            return

        # Increment all counters
        for key in self.counters:
            self.counters[key] += 1

        # Add random perturbation to direction
        self.direction = perturb_angle(self.direction, self.direction_perturbation)

        # Move in current direction
        dx, dy = vector_from_angle(self.direction, self.speed)
        new_x = self.position[0] + dx
        new_y = self.position[1] + dy

        # Handle boundaries
        if wrap:
            new_x = new_x % env_width
            new_y = new_y % env_height
        else:
            # Bounce off walls
            if new_x < 0 or new_x > env_width:
                self.direction = normalize_angle(np.pi - self.direction)
                new_x = np.clip(new_x, 0, env_width)
            if new_y < 0 or new_y > env_height:
                self.direction = normalize_angle(-self.direction)
                new_y = np.clip(new_y, 0, env_height)

        self.position = (new_x, new_y)

    def collision_with_target(self, target_type: str):
        """
        Handle collision with a target (resource or queen).

        Args:
            target_type: Type of target ('queen', 'red', 'green', 'blue')
        """
        # Reset counter for this target
        self.counters[target_type] = 0

        # If this was our objective, turn around and switch objective
        if target_type == self.current_objective:
            self.direction = normalize_angle(self.direction + np.pi)

            # Switch objective
            if self.carried_resource is not None:
                # Was carrying resource to queen, now go back for resource
                self.current_objective = self.carried_resource if not self.is_scout else None
                self.carried_resource = None
            else:
                # Was going to resource, now carrying it to queen
                self.carried_resource = target_type
                self.current_objective = 'queen'

    def receive_message(self, sender_position: Tuple[float, float], 
                       target_type: str, counter_value: int):
        """
        Receive a message from another agent and potentially update counter.

        Args:
            sender_position: Position of the agent sending the message
            target_type: Type of target the message is about
            counter_value: Counter value from sender + communication radius
        """
        if not self.alive:
            return False

        # Check if message improves our knowledge
        if counter_value < self.counters.get(target_type, float('inf')):
            # Calculate actual cost: distance to sender + their counter
            dist = distance(self.position, sender_position)
            new_counter = counter_value - self.communication_radius + dist + 1

            if new_counter < self.counters.get(target_type, float('inf')):
                self.counters[target_type] = int(new_counter)

                # If this target is our current objective, turn toward sender
                if target_type == self.current_objective:
                    self.direction = angle_between(self.position, sender_position)

                return True

        return False

    def get_broadcast_message(self) -> Dict[str, int]:
        """
        Get the message this agent broadcasts.

        Returns:
            Dictionary of target types to broadcast values
        """
        if not self.alive:
            return {}

        # Broadcast counter + communication radius for all targets
        return {
            target_type: counter + self.communication_radius
            for target_type, counter in self.counters.items()
        }

    def can_become_queen(self, nearest_queen_distance: float, 
                        queen_distance_threshold: float) -> bool:
        """
        Check if this agent can become a queen.

        Args:
            nearest_queen_distance: Distance to nearest queen
            queen_distance_threshold: Minimum distance required

        Returns:
            True if agent can become queen
        """
        return self.alive and nearest_queen_distance > queen_distance_threshold

    def __repr__(self):
        status = "carrying " + self.carried_resource if self.carried_resource else "searching"
        scout_str = " (scout)" if self.is_scout else ""
        return f"Agent{self.id}{scout_str} at {self.position}, {status}, objective={self.current_objective}"
