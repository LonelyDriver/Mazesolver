from mazesolver.src.pathfinding import Node
from mazesolver.src.timer import Timer
from queue import Queue
import logging

logger = logging.getLogger("App")
logger.setLevel(logging.DEBUG)

class BreathSolver:
    def __init__(self, param_list: list):
        logger.debug("Params list: %s", param_list)
        self._map = param_list[0]
        self._nodes = param_list[1]
        self._start = param_list[2]
        self._end = param_list[3]
        self._frontier = Queue()
        self._came_from = dict()
        self.Initialize()
        logger.debug("Start: {}".format(self._start.Pos))
        logger.debug("End: {}".format(self._end.Pos))

    def Initialize(self):
        self._frontier.put(self._start)
        self._came_from[self._start] = None

    @property
    def Map(self) -> list:
        return self._map

    @property
    def Frontier(self) -> Queue:
        return self._frontier
        
    def SolveStep(self):
        if self._start == None or self._end == None:
            logger.info("No start or end point")
            exit()

        if self._frontier.empty():
            logger.info("Queue empty")

        current = self._frontier.get()
        if current == self._end:
            logger.info("Found end!")
            return
        
        for next in current.Neighbours:
            if next not in self._came_from:
                self._frontier.put(next)
                self._came_from[next] = current

    @Timer(logging=logger.info)
    def Solve(self):
        with Timer():
            while not self._frontier.empty():
                self.SolveStep()

        current = self._end
        path = []
        while current != self._start:
            path.append(current)
            current = self._came_from[current]
        path.append(self._start)
        path.reverse()


        for node in path:
            logger.debug(node.Pos)
            x,y = node.Pos
            s = list(self._map[y])
            if s[x] != 'S' and s[x] != 'E':
                s[x] = 'X'
            self._map[y] = "".join(s)

        logger.info("Map")
        for index, row in enumerate(self._map):
            logger.info(row)
         