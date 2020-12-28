from mazesolver.src.pathfinding import MazeParser
from mazesolver.src.solve import BreathSolver
from mazesolver.src.ui import MazeApp
import json

if __name__ == "__main__":
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
    map_file = "mazesolver/src/maps/example.json"
    parser = MazeParser()
    #parser.InitializeFromJson(map_json)
    parser.LoadJsonFileAndInitialize(map_file)
    parser.CreateNodes()
    solver = BreathSolver(parser.GetParameters())
    solver.Solve()
    solver.PrintPath()
    