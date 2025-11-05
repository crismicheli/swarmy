"""
Unit tests for the Queen class.
"""
from swarmy.core.queen import Queen

def make_queen(**kwargs):
    return Queen(
        position=(0, 0),
        lifespan=1000,
        movement_speed=0.5,
        creation_cost={'red': 1, 'green': 1},
        life_extension_cost=1,
        agent_creation_probability=0.8,
        life_extension_probability=0.2,
        scout_creation_probability=0.2,
        **kwargs
    )

def test_queen_initialization():
    queen = make_queen()
    assert queen.lifespan == 1000
    assert queen.inventory == {'red': 0, 'green': 0}
    assert queen.alive

def test_queen_receive_resource():
    queen = make_queen()
    queen.receive_resource('red')
    assert queen.inventory['red'] == 1

def test_queen_can_create_agent_logic():
    queen = make_queen()
    queen.inventory['red'] = 1
    queen.inventory['green'] = 1
    assert queen.can_create_agent()

def test_queen_try_extend_life():
    queen = make_queen()
    queen.inventory['red'] = 2
    pre_life = queen.lifespan
    queen.try_extend_life()
    assert queen.lifespan >= pre_life
