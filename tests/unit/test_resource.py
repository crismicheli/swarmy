"""
Unit tests for the Resource class.
"""
from swarmy.core.resource import Resource

def make_resource(**kwargs):
    return Resource(
        position=(0, 0),
        resource_type='red',
        capacity=10,
        movement_speed=1.0,
        **kwargs
    )

def test_resource_initialization():
    res = make_resource()
    assert res.capacity == 10
    assert not res.depleted

def test_resource_harvesting():
    res = make_resource(capacity=2)
    ok = res.harvest(1)
    assert ok
    assert res.capacity == 1
    ok2 = res.harvest(1)
    assert not ok2
    assert res.depleted
