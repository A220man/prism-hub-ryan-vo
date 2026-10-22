import pytest
from app.models.instance import InstanceCreate, InstanceUpdate, InstanceStatus


def test_instance_create_validation():
    instance = InstanceCreate(name="Test", version="1.20.1")
    assert instance.name == "Test"
    assert instance.version == "1.20.1"
    assert instance.memory_min == 512
    assert instance.memory_max == 2048


def test_instance_create_memory_bounds():
    with pytest.raises(ValueError):
        InstanceCreate(name="Test", version="1.20.1", memory_min=100)
    with pytest.raises(ValueError):
        InstanceCreate(name="Test", version="1.20.1", memory_max=100)
    with pytest.raises(ValueError):
        InstanceCreate(name="Test", version="1.20.1", memory_min=20000)


def test_instance_update_partial():
    update = InstanceUpdate(name="New Name")
    assert update.name == "New Name"
    assert update.version is None
    assert update.memory_max is None


def test_instance_status_enum():
    assert InstanceStatus.CREATED == "created"
    assert InstanceStatus.READY == "ready"
    assert InstanceStatus.LAUNCHING == "launching"