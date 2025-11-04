"""
Spatial indexing utilities for efficient agent communication lookups.
"""
import numpy as np
from typing import List, Tuple, Set
from swarmy.core.agent import Agent

class GridCell:
    """A single cell in the spatial grid."""

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.agents: Set[int] = set()  # Agent IDs in this cell

    def add_agent(self, agent_id: int):
        """Add agent to this cell."""
        self.agents.add(agent_id)

    def remove_agent(self, agent_id: int):
        """Remove agent from this cell."""
        self.agents.discard(agent_id)

    def clear(self):
        """Clear all agents from cell."""
        self.agents.clear()


class SpatialGrid:
    """
    Spatial grid for efficient agent lookups by location.
    Divides environment into grid cells for O(1) nearest neighbor queries.
    """

    def __init__(self, width: float, height: float, cell_size: float):
        """
        Initialize spatial grid.

        Args:
            width: Environment width
            height: Environment height
            cell_size: Size of each grid cell
        """
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Calculate grid dimensions
        self.cols = int(np.ceil(width / cell_size))
        self.rows = int(np.ceil(height / cell_size))

        # Create grid
        self.grid = {}  # (row, col) -> GridCell
        self._init_grid()

    def _init_grid(self):
        """Initialize all grid cells."""
        for row in range(self.rows):
            for col in range(self.cols):
                self.grid[(row, col)] = GridCell(col, row)

    def _get_cell_coords(self, x: float, y: float) -> Tuple[int, int]:
        """Get grid cell coordinates for a position."""
        col = int(np.clip(x / self.cell_size, 0, self.cols - 1))
        row = int(np.clip(y / self.cell_size, 0, self.rows - 1))
        return row, col

    def add_agent(self, agent_id: int, x: float, y: float):
        """Add agent at position to grid."""
        row, col = self._get_cell_coords(x, y)
        self.grid[(row, col)].add_agent(agent_id)

    def remove_agent(self, agent_id: int, x: float, y: float):
        """Remove agent from grid."""
        row, col = self._get_cell_coords(x, y)
        self.grid[(row, col)].remove_agent(agent_id)

    def get_nearby_agents(self, x: float, y: float, radius: float) -> Set[int]:
        """
        Get all agents within radius of position.

        Args:
            x, y: Center position
            radius: Search radius

        Returns:
            Set of agent IDs within radius
        """
        center_row, center_col = self._get_cell_coords(x, y)

        # Determine cells to check
        cell_radius = int(np.ceil(radius / self.cell_size))
        nearby_agents = set()

        for row in range(
            max(0, center_row - cell_radius),
            min(self.rows, center_row + cell_radius + 1)
        ):
            for col in range(
                max(0, center_col - cell_radius),
                min(self.cols, center_col + cell_radius + 1)
            ):
                nearby_agents.update(self.grid[(row, col)].agents)

        return nearby_agents

    def clear(self):
        """Clear all agents from grid."""
        for cell in self.grid.values():
            cell.clear()

    def rebuild(self, agents: List[Agent]):
        """
        Rebuild grid with current agent positions.

        Args:
            agents: List of agents to add
        """
        self.clear()
        for agent in agents:
            if agent.alive:
                self.add_agent(agent.id, agent.position[0], agent.position[1])


class Quadtree:
    """
    Quadtree spatial index for hierarchical space partitioning.
    More efficient than grid for sparse agent distributions.
    """

    def __init__(self, x: float, y: float, width: float, height: float, max_depth: int = 8):
        """
        Initialize quadtree.

        Args:
            x, y: Top-left corner
            width, height: Bounds
            max_depth: Maximum tree depth
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_depth = max_depth

        self.agents: List[Tuple[int, float, float]] = []  # (agent_id, x, y)
        self.children = None  # Subdivisions
        self.depth = 0

    def insert(self, agent_id: int, x: float, y: float):
        """Insert agent at position."""
        self.agents.append((agent_id, x, y))

        # Subdivide if needed
        if len(self.agents) > 4 and self.depth < self.max_depth:
            self._subdivide()

    def _subdivide(self):
        """Subdivide into 4 quadrants."""
        half_w = self.width / 2
        half_h = self.height / 2

        self.children = [
            Quadtree(self.x, self.y, half_w, half_h, self.max_depth),  # NW
            Quadtree(self.x + half_w, self.y, half_w, half_h, self.max_depth),  # NE
            Quadtree(self.x, self.y + half_h, half_w, half_h, self.max_depth),  # SW
            Quadtree(self.x + half_w, self.y + half_h, half_w, half_h, self.max_depth),  # SE
        ]

        for child in self.children:
            child.depth = self.depth + 1

        # Redistribute agents
        old_agents = self.agents
        self.agents = []
        for agent_id, x, y in old_agents:
            self._insert_into_child(agent_id, x, y)

    def _insert_into_child(self, agent_id: int, x: float, y: float):
        """Insert into appropriate child quadrant."""
        if self.children is None:
            return

        half_w = self.width / 2
        half_h = self.height / 2

        # Determine quadrant
        if x < self.x + half_w:
            if y < self.y + half_h:
                quad = 0  # NW
            else:
                quad = 2  # SW
        else:
            if y < self.y + half_h:
                quad = 1  # NE
            else:
                quad = 3  # SE

        self.children[quad].insert(agent_id, x, y)

    def query_range(self, qx: float, qy: float, radius: float) -> Set[int]:
        """
        Query agents within radius.

        Args:
            qx, qy: Query center
            radius: Search radius

        Returns:
            Set of agent IDs
        """
        result = set()

        # Check if range intersects this node
        if not self._intersects_circle(qx, qy, radius):
            return result

        # Add agents in this node
        for agent_id, x, y in self.agents:
            dist_sq = (x - qx) ** 2 + (y - qy) ** 2
            if dist_sq <= radius ** 2:
                result.add(agent_id)

        # Check children
        if self.children is not None:
            for child in self.children:
                result.update(child.query_range(qx, qy, radius))

        return result

    def _intersects_circle(self, cx: float, cy: float, radius: float) -> bool:
        """Check if circle intersects this node's bounds."""
        # Find closest point in rectangle to circle center
        closest_x = np.clip(cx, self.x, self.x + self.width)
        closest_y = np.clip(cy, self.y, self.y + self.height)

        # Calculate distance
        dist_sq = (cx - closest_x) ** 2 + (cy - closest_y) ** 2
        return dist_sq <= radius ** 2
