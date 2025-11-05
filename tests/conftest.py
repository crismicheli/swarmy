"""
Pytest configuration for swarmy tests.
"""
import pytest

@pytest.fixture(autouse=True)
def run_around_tests():
    # Could set up/reset global state here if needed
    yield
    # Teardown actions
