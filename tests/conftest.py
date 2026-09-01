"""Shared pytest fixtures for the backend test suite."""

import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app

# Keep a pristine copy of the initial in-memory data so each test can restore
# it, since the app stores activities as module-level state.
_ORIGINAL_ACTIVITIES = copy.deepcopy(activities)


@pytest.fixture
def client():
    """Provide a TestClient with a freshly reset in-memory activities store."""
    # Arrange: reset the shared in-memory state before each test runs
    activities.clear()
    activities.update(copy.deepcopy(_ORIGINAL_ACTIVITIES))

    yield TestClient(app)

    # Cleanup: restore original state so other tests are unaffected
    activities.clear()
    activities.update(copy.deepcopy(_ORIGINAL_ACTIVITIES))
