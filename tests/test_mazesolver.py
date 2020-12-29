import json
from mazesolver.src.pathfinding import MazeParser
from mazesolver.src.solve import BreathSolver


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


def test_solve():
    parser = MazeParser()
    parser.InitializeFromJson(example_map_data())
    parser.CreateNodes()

    solver = BreathSolver(parser.GetMazeParameters())
    solver.Solve()
    assert True


def test_print_path_not_solved():
    parser = MazeParser()
    parser.InitializeFromJson(example_map_data())
    parser.CreateNodes()

    solver = BreathSolver(parser.GetMazeParameters())
    solver.PrintPath()
    assert True


def test_solved_path_shortest():
    shortest_path = ["   XXX    ",
                     "   EOX    ",
                     "    OX    ",
                     "   OXX    ",
                     "OOOXX     ",
                     "XXXX      ",
                     "XOO       ",
                     "XXXO      ",
                     "  XXOOOOOO",
                     "   XXXXXXS"]
    parser = MazeParser()
    parser.InitializeFromJson(example_map_data())
    parser.CreateNodes()

    solver = BreathSolver(parser.GetMazeParameters())
    solver.Solve()
    solver.PrintPath()

    solved_path = solver.Maze
    assert shortest_path == solved_path
