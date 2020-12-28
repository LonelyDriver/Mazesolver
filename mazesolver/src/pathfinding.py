import json
import logging
import sys

logger = logging.getLogger("App")

s_handler = logging.StreamHandler(sys.stdout)
f_handler = logging.FileHandler("pathfinding.log")
s_handler.setLevel(logging.DEBUG)
f_handler.setLevel(logging.ERROR)

s_format = logging.Formatter("%(asctime)s.%(msecs)03d Function: %(funcName)s %(levelname)s: %(message)s","%d.%m.%Y %H:%M:%S")
f_format = logging.Formatter("%(asctime)s.%(msecs)03d Function: %(funcName)s %(levelname)s: %(message)s","%d.%m.%Y %H:%M:%S")
s_handler.setFormatter(s_format)
f_handler.setFormatter(f_format)

logger.addHandler(s_handler)
logger.addHandler(f_handler)
logger.setLevel(logging.DEBUG)

class Node:
    '''
    This class represents a node. Every node has n neighbours
    which can be reached from the current node.
    Every node has a unique id.
    '''
    def __init__(self, id: int, pos: tuple, obstacle: bool):
        """
        param id   Unique node id
        param pos  X and Y position on map 
        """
        self._id = id
        self._pos = pos
        self._obstacle = obstacle
        self._neighbours = None
    @property
    def Neighbours(self) -> list:
        return self._neighbours

    @Neighbours.setter
    def Neighbours(self, value: list):
        self._neighbours = value

    @property
    def Id(self) -> int:
        return self._id

    @Id.setter
    def Id(self, value: int):
        self._id = id

    @property
    def Pos(self) -> tuple:
        return self._pos

    @Pos.setter
    def Pos(self, value: tuple):
        self._pos = pos
    
    @property
    def Obstacle(self) -> bool:
        return self._obstacle

    @Obstacle.setter
    def Obstace(self, obstacle):
        self._obstacle = obstacle

class MazeDto:
    def __init__(self):
        self._maze = []
        self._nodes = []
        self._start_node = None
        self._end_node = None

    @property
    def Maze(self) -> list:
        return self._maze

    @Maze.setter
    def Maze(self, maze: str):
        self._maze = maze
    
    @property
    def Nodes(self) -> list:
        return self._nodes
    
    @Nodes.setter
    def Nodes(self, nodes):
        self._nodes = nodes

    @property
    def StartNode(self) -> Node:
        return self._start_node

    @StartNode.setter
    def StartNode(self, start_node: Node):
        self._start_node = start_node

    @property
    def EndNode(self) -> Node:
        return self._end_node

    @EndNode.setter
    def EndNode(self, end_node: Node):
        self._end_node = end_node
    

class MazeParser:
    def __init__(self):
        self._maze = MazeDto()
        self._width = None
        self._max_tiles = None
        self._start = None
        self._end = None
        self._obstacle = None
        self._nodes = list()

    def GetMazeParameters(self) -> MazeDto:
        return self._maze

    def InitializeFromJson(self, map_json: str):
        if len(map_json) < 1:
            logger.warning("Invalid map json")
            raise ArithmeticError("Length of json object < 1")
        try:
            self._initializeMembersfromJson(map_json)
        except TypeError as e:
            logger.exception("TypeError: {}".format(e))
        except json.JSONDecodeError as e:
            logger.exception(e.msg)

    def LoadJsonFileAndInitialize(self, filename: str):
        try:
            maze_json = self._loadFile(filename)
            self._initializeMembersfromJson(maze_json)
        except OSError as err:
            logger.exception("OS error: {}".format(err))
        except:
            logger.exception("Unexpected error: {}".format(sys.exc_info()[0]))

    def _loadFile(self, filename) -> str:
        with open(filename, 'r') as f:
            map_json = f.read()
        return map_json

    def _initializeMembersfromJson(self, map_json: str):
        file = json.loads(map_json)

        logger.debug("File: %s", file)
        self._map = file['Map']
        self._maze.Maze = file['Map']
        logger.debug("Map: %s", self._map)
        self._start = file['Start']
        logger.debug("Start: %s", self._start)
        self._end = file['End']
        logger.debug("End: %s", self._end)
        self._width = len(self._map[0])
        logger.debug("Cols: %s", self._width)
        self._max_tiles = len(self._map) * self._width
        logger.debug("Tiles: %s", self._max_tiles)
        try:
            self._obstacle = file['Obstacle']
            logger.debug("Obstacles: %s", self._obstacle)
        except KeyError as e:
            logger.exception("No obstacle found")

    def CreateNodes(self):
        if len(self._maze.Maze) <1:
            logger.error("No map loaded")
            raise RuntimeError("No map loaded")
        try:
            self._createNodes()
            self._findNodeNeighbours()
        except:
            logger.exception("Unexpected error: {}".format(sys.exc_info()[0]))        
            
    def _createNodes(self):
        nodes = []
        for y, row in enumerate(self._maze.Maze):
            for x, col in enumerate(row):
                id = y*10+x
                pos = (x,y)
                obstacle = (col == self._obstacle)
                node = Node(id, pos, obstacle)
                self._nodes.append(node)
                nodes.append(node)
                if col == self._start:
                    self._maze.StartNode = node
                    logger.debug("Found start node: {}".format(node.Pos))
                elif col == self._end:
                    self._maze.EndNode = node
                    logger.debug("Found end node: {}".format(node.Pos))
        self._maze.Nodes = nodes

    def _findNodeNeighbours(self):
        for index, node in enumerate(self._maze.Nodes):
            n = list()
            n.append(index - self._width)
            n.append(index + self._width)
            if not (index % self._width == 0):
                n.append(index - 1)
            if not (index % self._width == self._width-1):
                n.append(index + 1)
            neighbours =    [self._maze.Nodes[index] for index in n 
                            if index >= 0 and index < self._max_tiles and not self._maze.Nodes[index].Obstacle]

            node.Neighbours = neighbours