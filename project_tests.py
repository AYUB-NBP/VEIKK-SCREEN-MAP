import pytest

from project import coordinates, pid_finder

def test_coordinates():
    assert coordinates(1) == [0,0,1920,1080]
    assert coordinates(0.5) == [480, 270, 1440, 810]
    assert coordinates(0) == [960, 540, 960, 540]

def test_pid_finder():
    assert pid_finder() != (0,0)

