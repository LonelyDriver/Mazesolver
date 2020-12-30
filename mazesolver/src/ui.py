import kivy
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager, CardTransition
from kivy.uix.button import Button
from kivy.properties import StringProperty, BooleanProperty
import logging
import sys

logger = logging.getLogger("App")

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
        self.behaviour = self._change_color
        self.field_type = Field.states[0]
        self.root = root

    def on_press(self):
        try:
            self.behaviour()
        except IndexError as err:
            logger.debug("IndexError: {}".format(err))

    def _change_color(self):
        for index, c in enumerate(self.colors):
            if self.color_index == index:
                self.color_index = (index+1) % len(self.colors)
                self.background_color = self.colors[self.color_index]
                self.changed = True
                break

    def on_release(self):
        if self.changed:
            self.changed = False

    def on_touch_move(self, touch):
        if not self.changed and self.collide_point(touch.x, touch.y):
            self.on_press()
        super().on_touch_move(touch)

    def on_touch_up(self, touch):
        self.on_release()

    def change_state(self, instance, value):
        self.color_index = 0

        if self.field_type == Field.states[0]:
            self.behaviour = self._mark_start
            self.field_type = Field.states[1]
        elif self.field_type == Field.states[1]:
            self.behaviour = self._mark_end
            self.field_type = Field.states[2]
        elif self.field_type == Field.states[2]:
            self.behaviour = self._change_color
        logger.debug("Behaviour changed: {}".format(self.behaviour))

    def reset_state(self, instace, value):
        self.color_index = 0
        self.behaviour = self._change_color

    def _mark_start(self):
        self.background_color = (1, 0, 0, 1)
        self.behaviour = self._do_nothing
        self.field_type = Field.states[3]
        self.root.state = Field.states[2]

    def _mark_end(self):
        self.background_color = (0, 1, 0, 1)
        self.behaviour = self._do_nothing
        self.field_type = Field.states[4]
        self.root.state = Field.states[0]

    def _do_nothing(self):
        pass


class HomeScreen(Screen):
    state = StringProperty("obstacle")
    reset = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        for _ in range(self.ids['maze'].cols*self.ids['maze'].rows):
            field = Field(self)
            self.bind(state=field.change_state)
            self.ids['maze'].add_widget(field)


class PropertiesScreen(Screen):
    def __init__(self, homescreen, **kwargs):
        super().__init__(**kwargs)
        self.homescreen = homescreen

    def changeState(self):
        self.homescreen.state = "mark_start"


class MazeApp(App):
    def build(self):
        sm = ScreenManager(transition=CardTransition())
        homescreen = HomeScreen(name="menu")
        propertyscreen = PropertiesScreen(homescreen, name="properties")

        sm.add_widget(homescreen)
        sm.add_widget(propertyscreen)

        return sm
