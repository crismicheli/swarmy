"""
Unit tests for the Agent class.
"""
import pytest
from swarmy.core.agent import Agent

def make_agent(**kwargs):
    return Agent(
        position=(0, 0),
        speed=1.0,
        communication_radius=40,
        direction_perturbation=0.05,
        lifespan=1000,
        resource_types=['red', 'green'],
        is_scout=False,
        assigned_resource='red',
        **kwargs
    )

def test_agent_initialization():
    agent = make_agent()
    assert agent.position == (0, 0)
    assert agent.speed == 1.0
    assert isinstance(agent.counters, dict)
    assert agent.alive

def test_agent_step_increments_age():
    agent = make_agent()
    pre_age = agent.age
    agent.step(100, 100)
    assert agent.age == pre_age + 1

def test_agent_lifespan():
    agent = make_agent(lifespan=1)
    agent.step(100, 100)
    assert not agent.alive


def test_collision_with_target_resets_counter():
    agent = make_agent()
    agent.counters['queen'] = 10
    agent.collision_with_target('queen')
    assert agent.counters['queen'] == 0


def test_receive_message_updates_counters():
    agent = make_agent()
    other_pos = (1, 1)
    updated = agent.receive_message(other_pos, 'red', 2)
    assert updated
    assert agent.counters['red'] < 500  # Should be updated
