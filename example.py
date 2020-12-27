from mazesolver.src.pathfinding import MapCreator
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

    c = MapCreator()
    c.Load(map_json)
    c.CreateNodes()
    breath = BreathSolver(c.Params())
    breath.Solve()
    """
    c.Load("src/maps/example.json")
    c.CreateNodes()
    params = c.Params()
    breath = BreathSolver(params)
    breath.Solve()
    MazeApp().run()
    """

