import json
from mazesolver.src.pathfinding import MazeParser


def example_map_data() -> str:
    map_file = dict()
    map_file["Start"] = "S"
    map_file["End"] = "E"
    map_file["Path"] = " "
    map_file["Obstacle"] = "O"
    map_file["Map"] = ["          ",
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


def test_loading_json():
    MazeParser().InitializeFromJson(example_map_data())
    assert True


def test_loading_json_none():
    try:
        MazeParser().InitializeFromJson(None)
        assert(False)
    except TypeError:
        assert True


def test_loading_json_no_start():
    try:
        data = example_map_data()
        data_json = json.loads(data)
        del data_json['Start']

        MazeParser().InitializeFromJson(json.dumps(data_json))
        assert False
    except KeyError:
        assert True


def test_loading_json_no_obstacle():
    data = example_map_data()
    data_json = json.loads(data)
    del data_json['Obstacle']

    MazeParser().InitializeFromJson(json.dumps(data_json))
    assert True


def test_create_nodes_without_initialzation():
    try:
        parser = MazeParser()
        parser.CreateNodes()
        assert False
    except RuntimeError:
        assert True


def test_create_nodes():
    parser = MazeParser()
    parser.InitializeFromJson(example_map_data())
    parser.CreateNodes()
    assert True


def test_get_parameters():
    parser = MazeParser()
    parser.InitializeFromJson(example_map_data())
    parser.CreateNodes()

    params = parser.GetMazeParameters()

    assert params.StartNode.Pos == (9, 9)
    assert params.EndNode.Pos == (3, 1)
    assert len(params.Nodes) == 100
