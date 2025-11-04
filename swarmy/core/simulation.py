"""
Main simulation engine for Swarmy.
"""
import numpy as np
from typing import List, Dict, Optional, Tuple
from swarmy.core.agent import Agent
from swarmy.core.queen import Queen
from swarmy.core.resource import Resource
from swarmy.core.utils import distance
from swarmy.config.config import SimulationConfig

class SwarmSimulation:
    """
    Main simulation class that orchestrates agents, queens, and resources.
    """

    def __init__(self, config: SimulationConfig):
        """
        Initialize simulation with configuration.

        Args:
            config: SimulationConfig object with all parameters
        """
        self.config = config
        self.step_count = 0

        # Initialize collections
        self.agents: List[Agent] = []
        self.queens: List[Queen] = []
        self.resources: List[Resource] = []

        # Communication tracking (for visualization)
        self.recent_communications = []  # List of (agent1_id, agent2_id) tuples

        # Initialize simulation
        self._initialize()

    def _initialize(self):
        """Set up initial simulation state."""
        # Create queens
        for i in range(self.config.num_queens):
            pos = (
                np.random.uniform(0, self.config.width),
                np.random.uniform(0, self.config.height)
            )
            queen = Queen(
                position=pos,
                lifespan=self.config.queen_initial_lifespan,
                movement_speed=self.config.queen_movement_speed,
                creation_cost=self.config.queen_creation_cost,
                life_extension_cost=self.config.queen_lifespan_extension_cost,
                agent_creation_probability=self.config.agent_creation_probability,
                life_extension_probability=self.config.life_extension_probability,
                scout_creation_probability=self.config.scout_creation_probability
            )
            self.queens.append(queen)

        # Create resources
        for i in range(self.config.num_resources):
            pos = (
                np.random.uniform(0, self.config.width),
                np.random.uniform(0, self.config.height)
            )
            rtype = self.config.resource_types[i % len(self.config.resource_types)]
            capacity = np.random.randint(
                self.config.resource_capacity_min,
                self.config.resource_capacity_max
            )
            resource = Resource(
                position=pos,
                resource_type=rtype,
                capacity=capacity,
                movement_speed=self.config.resource_movement_speed
            )
            self.resources.append(resource)

        # Create worker agents
        num_workers = self.config.num_agents - self.config.num_scouts
        for i in range(num_workers):
            pos = self.queens[0].position if self.queens else (
                np.random.uniform(0, self.config.width),
                np.random.uniform(0, self.config.height)
            )
            speed = np.random.uniform(
                self.config.agent_speed_min,
                self.config.agent_speed_max
            )
            lifespan = np.random.randint(
                self.config.agent_lifespan_min,
                self.config.agent_lifespan_max
            )
            assigned = self.config.resource_types[i % len(self.config.resource_types)]

            agent = Agent(
                position=pos,
                speed=speed,
                communication_radius=self.config.communication_radius,
                direction_perturbation=self.config.direction_perturbation,
                lifespan=lifespan,
                resource_types=self.config.resource_types,
                is_scout=False,
                assigned_resource=assigned
            )
            self.agents.append(agent)

        # Create scout agents
        for i in range(self.config.num_scouts):
            pos = self.queens[0].position if self.queens else (
                np.random.uniform(0, self.config.width),
                np.random.uniform(0, self.config.height)
            )
            speed = np.random.uniform(
                self.config.agent_speed_min,
                self.config.agent_speed_max
            )
            lifespan = np.random.randint(
                self.config.agent_lifespan_min,
                self.config.agent_lifespan_max
            )

            agent = Agent(
                position=pos,
                speed=speed,
                communication_radius=self.config.communication_radius,
                direction_perturbation=self.config.direction_perturbation,
                lifespan=lifespan,
                resource_types=self.config.resource_types,
                is_scout=True
            )
            self.agents.append(agent)

    def step(self):
        """Execute one simulation time step."""
        self.step_count += 1
        self.recent_communications = []

        # 1. Move all agents
        for agent in self.agents:
            if agent.alive:
                agent.step(self.config.width, self.config.height, 
                          self.config.wrap_boundaries)

        # 2. Move resources
        for resource in self.resources:
            if not resource.depleted:
                resource.step(self.config.width, self.config.height,
                            self.config.wrap_boundaries)

        # 3. Update queens
        for queen in self.queens:
            if queen.alive:
                # Find furthest resource
                furthest_resource_pos = self._get_furthest_resource_position(queen)
                queen.step(furthest_resource_pos, self.config.width, 
                          self.config.height, self.config.wrap_boundaries)

        # 4. Check collisions and handle interactions
        self._handle_collisions()

        # 5. Process agent communications
        self._process_communications()

        # 6. Queens try to create agents or extend life
        new_agents = []
        for queen in self.queens:
            if queen.alive:
                # Try to create agent
                agent_params = queen.try_create_agent()
                if agent_params:
                    new_agents.append(agent_params)

                # Try to extend life
                queen.try_extend_life()

        # Create new agents
        for params in new_agents:
            self._create_agent(**params)

        # 7. Check for new queen emergence
        self._check_queen_emergence()

        # 8. Remove dead agents and queens
        self.agents = [a for a in self.agents if a.alive]
        self.queens = [q for q in self.queens if q.alive]

        # 9. Replenish depleted resources (optional)
        self._replenish_resources()

    def _handle_collisions(self):
        """Check and handle collisions between agents and targets."""
        for agent in self.agents:
            if not agent.alive:
                continue

            # Check collision with resources
            for resource in self.resources:
                if resource.depleted:
                    continue

                dist = distance(agent.position, resource.position)
                collision_dist = self.config.agent_radius + self.config.resource_radius

                if dist < collision_dist:
                    # Agent collided with resource
                    if agent.carried_resource is None:
                        # Pick up resource
                        if resource.harvest(1):
                            agent.collision_with_target(resource.resource_type)
                    break

            # Check collision with queens
            for queen in self.queens:
                if not queen.alive:
                    continue

                dist = distance(agent.position, queen.position)
                collision_dist = self.config.agent_radius + self.config.queen_radius

                if dist < collision_dist:
                    # Agent collided with queen
                    if agent.carried_resource is not None:
                        # Deliver resource
                        queen.receive_resource(agent.carried_resource)
                        agent.collision_with_target('queen')
                    else:
                        # Just touching queen, reset queen counter
                        agent.counters['queen'] = 0
                    break

    def _process_communications(self):
        """Process agent-to-agent communication."""
        alive_agents = [a for a in self.agents if a.alive]

        for i, sender in enumerate(alive_agents):
            # Get sender's broadcast message
            messages = sender.get_broadcast_message()

            # Check which agents can hear
            for j, receiver in enumerate(alive_agents):
                if i == j or not receiver.alive:
                    continue

                dist = distance(sender.position, receiver.position)
                if dist <= self.config.communication_radius:
                    # Receiver is in range
                    for target_type, value in messages.items():
                        updated = receiver.receive_message(
                            sender.position, target_type, value
                        )
                        if updated:
                            self.recent_communications.append((sender.id, receiver.id))

    def _get_furthest_resource_position(self, queen: Queen) -> Optional[Tuple[float, float]]:
        """Find the position of the furthest resource from a queen."""
        max_dist = -1
        furthest_pos = None

        for resource in self.resources:
            if resource.depleted:
                continue
            dist = distance(queen.position, resource.position)
            if dist > max_dist:
                max_dist = dist
                furthest_pos = resource.position

        return furthest_pos

    def _check_queen_emergence(self):
        """Check if any agent is far enough from queens to become a new queen."""
        for agent in self.agents:
            if not agent.alive:
                continue

            # Find distance to nearest queen
            min_dist = float('inf')
            for queen in self.queens:
                if queen.alive:
                    dist = distance(agent.position, queen.position)
                    min_dist = min(min_dist, dist)

            # Check if agent can become queen
            if agent.can_become_queen(min_dist, self.config.queen_distance_threshold):
                # Transform agent into queen
                new_queen = Queen(
                    position=agent.position,
                    lifespan=self.config.queen_initial_lifespan // 2,  # Start with half life
                    movement_speed=self.config.queen_movement_speed,
                    creation_cost=self.config.queen_creation_cost,
                    life_extension_cost=self.config.queen_lifespan_extension_cost,
                    agent_creation_probability=self.config.agent_creation_probability,
                    life_extension_probability=self.config.life_extension_probability,
                    scout_creation_probability=self.config.scout_creation_probability
                )
                self.queens.append(new_queen)
                agent.alive = False  # Remove agent
                break  # Only one emergence per step

    def _create_agent(self, position: Tuple[float, float], 
                     is_scout: bool, assigned_resource: Optional[str]):
        """Create a new agent."""
        speed = np.random.uniform(
            self.config.agent_speed_min,
            self.config.agent_speed_max
        )
        lifespan = np.random.randint(
            self.config.agent_lifespan_min,
            self.config.agent_lifespan_max
        )

        agent = Agent(
            position=position,
            speed=speed,
            communication_radius=self.config.communication_radius,
            direction_perturbation=self.config.direction_perturbation,
            lifespan=lifespan,
            resource_types=self.config.resource_types,
            is_scout=is_scout,
            assigned_resource=assigned_resource
        )
        self.agents.append(agent)

    def _replenish_resources(self):
        """Replenish depleted resources (optional, configurable)."""
        # Remove fully depleted resources and add new ones with some probability
        if len(self.resources) < self.config.num_resources:
            if np.random.random() < 0.01:  # 1% chance per step
                pos = (
                    np.random.uniform(0, self.config.width),
                    np.random.uniform(0, self.config.height)
                )
                rtype = np.random.choice(self.config.resource_types)
                capacity = np.random.randint(
                    self.config.resource_capacity_min,
                    self.config.resource_capacity_max
                )
                resource = Resource(
                    position=pos,
                    resource_type=rtype,
                    capacity=capacity,
                    movement_speed=self.config.resource_movement_speed
                )
                self.resources.append(resource)

    def get_state(self) -> Dict:
        """
        Get complete simulation state for visualization or analysis.

        Returns:
            Dictionary with all simulation state information
        """
        return {
            'step': self.step_count,
            'agents': [
                {
                    'id': a.id,
                    'position': a.position,
                    'direction': a.direction,
                    'is_scout': a.is_scout,
                    'carried_resource': a.carried_resource,
                    'current_objective': a.current_objective,
                    'alive': a.alive,
                    'age_ratio': a.age / a.max_age
                }
                for a in self.agents
            ],
            'queens': [
                {
                    'id': q.id,
                    'position': q.position,
                    'health_ratio': q.get_health_ratio(),
                    'inventory': q.inventory,
                    'alive': q.alive
                }
                for q in self.queens
            ],
            'resources': [
                {
                    'id': r.id,
                    'position': r.position,
                    'resource_type': r.resource_type,
                    'depletion_ratio': r.get_depletion_ratio(),
                    'depleted': r.depleted
                }
                for r in self.resources
            ],
            'communications': self.recent_communications
        }

    def add_agent(self, **kwargs):
        """Add a new agent to the simulation."""
        agent = Agent(**kwargs)
        self.agents.append(agent)
        return agent

    def add_queen(self, **kwargs):
        """Add a new queen to the simulation."""
        queen = Queen(**kwargs)
        self.queens.append(queen)
        return queen

    def add_resource(self, **kwargs):
        """Add a new resource to the simulation."""
        resource = Resource(**kwargs)
        self.resources.append(resource)
        return resource
