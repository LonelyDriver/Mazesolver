import kivy
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager, CardTransition
from kivy.uix.button import Button
from kivy.properties import BooleanProperty, ObjectProperty
from mazesolver.src.pathfinding import MazeParser
from mazesolver.src.solve import BreathSolver
import logging
import sys
import enum
import json

logger = logging.getLogger("Ui")

s_handler = logging.StreamHandler(sys.stdout)
f_handler = logging.FileHandler("pathfinding.log")
s_handler.setLevel(logging.DEBUG)
f_handler.setLevel(logging.ERROR)

s_format = logging.Formatter(
    "%(asctime)s.%(msecs)03d Function: "
    "%(funcName)s %(levelname)s: %(message)s",
    "%d.%m.%Y %H:%M:%S")

f_format = logging.Formatter(
    "%(asctime)s.%(msecs)03d Function: "
    "%(funcName)s %(levelname)s: %(message)s",
    "%d.%m.%Y %H:%M:%S")

s_handler.setFormatter(s_format)
f_handler.setFormatter(f_format)

logger.addHandler(s_handler)
logger.addHandler(f_handler)
logger.setLevel(logging.DEBUG)

kivy.require("2.0.0")


class FieldStates(enum.Enum):
    Obstacle = 0
    Empty = 1
    Start = 2
    End = 3


class GridStates(enum.Enum):
    Normal = 0
    MarkStart = 1
    MarkEnd = 2


class Field(Button):
    states = ["obstacle",
              "mark_start",
              "mark_end",
              "start",
              "end"]

    def __init__(self, root, **kwargs):
        super().__init__(**kwargs)
        self.color_index = 0
        self.background_color = self.colors[self.color_index]
        self.changed = False
        self.behaviour = self._change_color_and_state
        self.field_type = FieldStates.Empty
        self.root = root

    def on_touch_move(self, touch):
        if not self.changed and self.collide_point(touch.x, touch.y):
            self.on_press()
            return
        super().on_touch_move(touch)

    def on_press(self):
        try:
            self.behaviour()
        except IndexError as err:
            logger.debug("IndexError: {}".format(err))

    def on_touch_up(self, touch):
        self.on_release()

    def on_release(self):
        if self.changed:
            self.changed = False

    def reset_field(self):
        self.field_type = FieldStates.Empty
        self.color_index = 0
        self.background_color = self.colors[self.color_index]

    def change_state(self, instance, value):
        self.color_index = 0

        if (self.field_type == FieldStates.Start or
                self.field_type == FieldStates.End):
            return

        if self.root.state == GridStates.MarkStart:
            self.behaviour = self._mark_start
        elif self.root.state == GridStates.MarkEnd:
            self.behaviour = self._mark_end
        elif self.root.state == GridStates.Normal:
            self.behaviour = self._change_color_and_state
        logger.debug("Behaviour changed: {}".format(self.behaviour))

    def _mark_start(self):
        self.background_color = (1, 0, 0, 1)
        self.behaviour = self._do_nothing
        self.field_type = FieldStates.Start
        self.root.state = GridStates.MarkEnd

    def _mark_end(self):
        self.background_color = (0, 1, 0, 1)
        self.behaviour = self._do_nothing
        self.field_type = FieldStates.End
        self.root.state = GridStates.Normal

    def _do_nothing(self):
        pass

    def _change_color_and_state(self):
        try:
            self._change_color()
            self._change_state()
        except KeyError as err:
            logger.exception("KeyError: {}".format(err))

    def _change_color(self):
        for index, c in enumerate(self.colors):
            if self.color_index == index:
                self.color_index = (index+1) % len(self.colors)
                self.background_color = self.colors[self.color_index]
                self.changed = True
                break

    def _change_state(self):
        states = [FieldStates.Empty, FieldStates.Obstacle]
        self.field_type = states[self.color_index]
        logger.debug("Type: {}".format(self.field_type))

    @property
    def Type(self) -> enum.Enum:
        return self.field_type


class HomeScreen(Screen):
    state = ObjectProperty(GridStates.Normal)
    reset = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.maze = {}
        self.maze["Start"] = "S"
        self.maze["End"] = "E"
        self.maze["Obstacle"] = "O"
        self.maze["Path"] = " "

        for _ in range(self.ids.maze.cols*self.ids.maze.rows):
            field = Field(self)
            self.bind(state=field.change_state)
            self.ids['maze'].add_widget(field)

    def reset_grid(self):
        for child in self.ids.maze.children:
            child.reset_field()
        HomeScreen.state = GridStates.Normal

    def solve(self):
        try:
            maze_json = self._create_json_from_grid()
            parser = MazeParser()
            parser.InitializeFromJson(maze_json)
            parser.CreateNodes()
            maze_params = parser.GetMazeParameters()
            solver = BreathSolver(maze_params)
            solver.Solve()
            solver.PrintPath()
        except RuntimeError as err:
            logger.exception("RuntimeError: {}".format(err))
        except ArithmeticError as err:
            logger.exception("ArithmeticError: {}".format(err))

    def _create_json_from_grid(self) -> str:
        maze = []
        row = []
        logger.debug("Cols: {}".format(self.ids.maze.cols))
        for index, child in reversed(list(enumerate(self.ids.maze.children))):
            if child.Type == FieldStates.Empty:
                row.append(" ")
            elif child.Type == FieldStates.Obstacle:
                row.append("O")
            elif child.Type == FieldStates.Start:
                row.append("S")
            elif child.Type == FieldStates.End:
                row.append("E")
            else:
                logger.error("Undefined field state")
                raise RuntimeError("Undefined field state")
            if index % self.ids.maze.cols == 0:
                maze.append("".join(row))
                row = []
        self.maze["Map"] = maze

        logger.debug("MAZE:\n{}".format(maze))
        for row in self.maze["Map"]:
            logger.debug("{}".format(row))
        return json.dumps(self.maze)


class PropertiesScreen(Screen):
    def __init__(self, homescreen, **kwargs):
        super().__init__(**kwargs)
        self.homescreen = homescreen

    def changeState(self):
        self.homescreen.state = GridStates.MarkStart

    def reset(self):
        self.homescreen.reset_grid()


class MazeApp(App):
    def build(self):
        sm = ScreenManager(transition=CardTransition())
        homescreen = HomeScreen(name="menu")
        propertyscreen = PropertiesScreen(homescreen, name="properties")

        sm.add_widget(homescreen)
        sm.add_widget(propertyscreen)

        return sm
