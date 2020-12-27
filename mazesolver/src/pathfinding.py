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
    This class represents a node. Every node hast n neighbours which can be reached from the current node.
    Every node needs has a unique id.
    '''
    def __init__(self, id: int, pos: tuple, obstacle: bool):
        """
        \param id   Unique node id
        \param pos  X and Y position on map 
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

class MapCreator:
    def __init__(self):
        self._map = None
        self._width = None
        self._max_tiles = None
        self._start = None
        self._start_node = None
        self._end = None
        self._end_node = None
        self._obstacle = None
        self._nodes = list()

    def Params(self) -> list:
        return [self._map, self._nodes, self._start_node, self._end_node]

    def Load(self, mapJson: str):
        if len(mapJson) < 1:
            logger.warning("Invalid map json")
            raise ArithmeticError("Length of json object < 1")
        try:
            file = json.loads(mapJson)
            logger.debug("File: %s", file)
            self._map = file['Map']
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
        except TypeError as e:
            logger.exception(e.msg)
        except json.JSONDecodeError as e:
            logger.exception(e.msg)


    def LoadJsonFile(self, filename: str):
        if len(filename) < 1:
            logger.warning("Invalid filename")
            exit()
        
        with open(filename, 'r') as f:
            file = f.read()
            logger.debug("File: %s",file)
            file = json.loads(file)
            logger.debug("File: %s",file)
            self._map = file['Map']
            logger.debug("Map: %s", self._map)
            self._start = file['Start']
            logger.debug("Start: %s", self._start)
            self._end = file['End']
            logger.debug("End: %s", self._end)
            self._width = len(self._map[0])
            logger.debug("Cols: %s", self._width)
            self._max_tiles = len(self._map) * self._width
            try:
                self._obstacle = file['Obstacle']
            except KeyError as e:
                logger.exception("No obstacle found")

    def CreateNodes(self):
        if self._map == None:
            logger.error("No map loaded")
            exit()
        # create all nodes
        for y, row in enumerate(self._map):
            for x, col in enumerate(row):
                id = y*10+x
                pos = (x,y)
                obstacle = (col == self._obstacle)
                node = Node(id, pos, obstacle)
                self._nodes.append(node)
                if col == self._start:
                    self._start_node = node
                    logger.debug("Found start node: {}".format(node.Pos))
                elif col == self._end:
                    self._end_node = node
                    logger.debug("Found end node: {}".format(node.Pos))

        #find neighbours
        for index, node in enumerate(self._nodes):
            n = list()
            n.append(index - self._width)
            n.append(index + self._width)
            if not (index % self._width == 0):
                n.append(index - 1)
            if not (index % self._width == self._width-1):
                n.append(index + 1)
            neighbours =    [self._nodes[index] for index in n 
                            if index >= 0 and index < self._max_tiles and not self._nodes[index].Obstacle]

            node.Neighbours = neighbours
            
