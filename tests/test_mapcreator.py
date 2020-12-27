from src.pathfinding import MapCreator
import pytest

@pytest.fixture
def example_map_data():
    map_file = dict()
    map_file["Start"] = "S"
    map_file["End"] = "E"
    map_file["Path"] = " "
    map_file["Obstacle"] = "O"
    map_file["Map"] =  ["          ",
                        "   EO     ",
                        "    O     ",
                        "   O      ",
                        "OOO       ",
                        "          ",
                        " OO       ",
                        "   O      ",
                        "    OOOOOO",
                        "         S"]
    map_json = json.dumps(map_file)

    return map_json

def test_loading_json_function():
    params  = MapCreator().Load(mapJson).Params()
    
