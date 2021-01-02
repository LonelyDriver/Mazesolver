from mazesolver.src.pathfinding import MazeDto
from mazesolver.src.timer import Timer
from mazesolver.src.exceptions import SolveError
from queue import Queue
import logging

logger = logging.getLogger("App")
logger.setLevel(logging.DEBUG)


class BreathSolver:
    def __init__(self):
        self._maze = None
        self._frontier = Queue()
        self._came_from = dict()
        self._path = []

    def Initialize(self, maze_object: MazeDto):
        self._maze = maze_object
        if maze_object is None or len(maze_object.Maze) < 1 or len(maze_object.Nodes) < 1:
            raise SolveError(TypeError("Can not initialize from NoneType"), self.Initialize.__name__)
        if self._maze.StartNode is None or self._maze.EndNode is None:
            raise SolveError(AttributeError("Start or end node not found"), self.Initialize.__name__)

        self._frontier.put(self._maze.StartNode)
        self._came_from[self._maze.StartNode] = None

    @property
    def Maze(self) -> list:
        return self._maze.Maze

    @property
    def Frontier(self) -> Queue:
        return self._frontier

    @property
    def Path(self) -> list:
        return self._path

    @Timer(logging=logger.info)
    def Solve(self):
        while not self._frontier.empty():
            self.SolveStep()

    def SolveStep(self):
        current = self._frontier.get()
        if current == self._maze.EndNode:
            logger.info("Found end!")
            return

        for next in current.Neighbours:
            if next not in self._came_from:
                self._frontier.put(next)
                self._came_from[next] = current

    def PrintPath(self):
        self.CreatePath()
        logger.info("Way out:")
        for index, row in enumerate(self._maze.Maze):
            logger.info(row)

    def CreatePath(self):
        try:
            self._createPath()
        except KeyError as err:
            logger.exception("KeyError: {}".format(err))
            raise SolveError(err, self._createPath.__name__)

    def _createPath(self):
        current = self._maze.EndNode
        path = []
        while current != self._maze.StartNode:
            path.append(current)
            current = self._came_from[current]
        path.append(self._maze.StartNode)
        path.reverse()
        self._path = path

        for node in path:
            x, y = node.Pos
            s = list(self._maze.Maze[y])
            if s[x] != 'S' and s[x] != 'E':
                s[x] = 'X'
            self._maze.Maze[y] = "".join(s)
