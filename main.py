import gc

from kivy.app import App
from kivy.core.window import Window

from layout import MainContainer

Window.size = (1400, 700)
Window.top = 200
Window.left = 200
Window.clearcolor = "#9CAFAA"


class MainApp(App):
    def build(self):
        self.title = "Knowledge Representation and Reasoning"
        return MainContainer()


if __name__ == "__main__":
    gc.set_threshold(2, 2, 2)
    app = MainApp()
    app.run()
