import kivy


from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.button import Button

kivy.require("2.0.0")


class Field(Button):
    colors = [(0.722, 0.682, 0.784, 1), (0.235, 0.204, 0.361, 1)]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color_index = 0
        self.background_color = Field.colors[self.color_index]
        self.changed = False

    def on_press(self):
        for index, c in enumerate(Field.colors):
            if self.color_index == index:
                print("{}:{}".format(index, c))
                self.color_index = (index+1) % len(Field.colors)
                self.background_color = Field.colors[self.color_index]
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


class MazeSheets(ScreenManager):
    pass


class HomeSheet(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        for _ in range(self.ids['maze'].cols*self.ids['maze'].rows):
            self.ids['maze'].add_widget(Field())


class Maze:
    pass


class MazeApp(App):
    def build(self):
        return HomeSheet()
