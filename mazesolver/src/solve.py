from mazesolver.src.pathfinding import Node, MazeDto
from mazesolver.src.timer import Timer
from queue import Queue
import logging

logger = logging.getLogger("App")
logger.setLevel(logging.DEBUG)

class BreathSolver:
    def __init__(self, maze_object: MazeDto):
        self._maze = maze_object
        self._frontier = Queue()
        self._came_from = dict()
        self.Initialize()
        logger.debug("Start: {}".format(self._maze.StartNode.Pos))
        logger.debug("End: {}".format(self._maze.EndNode.Pos))

    def Initialize(self):
        self._frontier.put(self._maze.StartNode)
        self._came_from[self._maze.StartNode] = None

    @property
    def Maze(self) -> list:
        return self._maze.Maze

    @property
    def Frontier(self) -> Queue:
        return self._frontier
        
    def SolveStep(self):
        if self._maze.StartNode == None or self._maze.EndNode == None:
            logger.info("No start or end point")
            raise RuntimeError("Start or end node invalid")

        current = self._frontier.get()
        if current == self._maze.EndNode:
            logger.info("Found end!")
            return
        
        for next in current.Neighbours:
            if next not in self._came_from:
                self._frontier.put(next)
                self._came_from[next] = current

    @Timer(logging=logger.info)
    def Solve(self):
        try:
            while not self._frontier.empty():
                self.SolveStep()
        except Empty as e:
            logger.exception("Queue is empty")
        except RuntimeError as e:
            logger.exception(e.msg())
        except:
            logger.exception("Unexpected error: {}".format(sys.exc_info()[0]))

    def PrintPath(self):
        try:
            self._createPath()
            logger.info("Way out:")
            for index, row in enumerate(self._maze.Maze):
                logger.info(row)
        except:
            logger.exception("Unexpected error: {}".format(sys.exc_info()[0]))

    def _createPath(self):
        current = self._maze.EndNode
        path = []
        while current != self._maze.StartNode:
            path.append(current)
            current = self._came_from[current]
        path.append(self._maze.StartNode)
        path.reverse()

        for node in path:
            x,y = node.Pos
            s = list(self._maze.Maze[y])
            if s[x] != 'S' and s[x] != 'E':
                s[x] = 'X'
            self._maze.Maze[y] = "".join(s)