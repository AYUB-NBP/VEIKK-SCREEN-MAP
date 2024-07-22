from project import coordinates,pid_finder, factor
import project
from unittest.mock import Mock

def test_coordinates():
    assert coordinates(1) == [0,0,1920,1080]
    assert coordinates(0.5) == [480, 270, 1440, 810]
    assert coordinates(0) == [960, 540, 960, 540]

def test_pid_finder():
    assert pid_finder() != (0,0)

# --------------------------------------------------

#   Define what Function to test:

def test_factor():
    #Create mock object:
    mock_arg = Mock()
    #Set the return value from Mock object.
    mock_arg.return_value = '0.5'
    #Plug the object as a return value to the dependency function
    project.sys.argv[1] = mock_arg()
    #Call functin we're testing 
    result = factor()
    #assert the mock object was called once
    mock_arg.assert_called_once()
    #Assert result matches expected result
    assert result == 0.5