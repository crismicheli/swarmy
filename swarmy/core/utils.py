"""
Utility functions for geometric and mathematical operations.
"""
import numpy as np
from typing import Tuple

def distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    """Calculate Euclidean distance between two points."""
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def angle_between(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    """Calculate angle from p1 to p2 in radians."""
    return np.arctan2(p2[1] - p1[1], p2[0] - p1[0])

def normalize_angle(angle: float) -> float:
    """Normalize angle to [-pi, pi] range."""
    return (angle + np.pi) % (2 * np.pi) - np.pi

def perturb_angle(angle: float, max_perturbation: float) -> float:
    """Add random perturbation to angle."""
    perturbation = np.random.uniform(-max_perturbation, max_perturbation)
    return normalize_angle(angle + perturbation)

def vector_from_angle(angle: float, magnitude: float = 1.0) -> Tuple[float, float]:
    """Convert angle and magnitude to 2D vector."""
    return (magnitude * np.cos(angle), magnitude * np.sin(angle))

def wrap_position(pos: Tuple[float, float], width: float, height: float) -> Tuple[float, float]:
    """Wrap position to stay within bounds (toroidal topology)."""
    return (pos[0] % width, pos[1] % height)

def clip_position(pos: Tuple[float, float], width: float, height: float) -> Tuple[float, float]:
    """Clip position to stay within bounds."""
    x = np.clip(pos[0], 0, width)
    y = np.clip(pos[1], 0, height)
    return (x, y)
