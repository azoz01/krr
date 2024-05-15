import gc

from kivy.app import App
from kivy.core.window import Window

from layout import MainContainer

Window.size = (1024, 700)
Window.clearcolor = "#9CAFAA"


class MainApp(App):
    def build(self):
        self.title = "Knowledge Representation and Reasoning"
        return MainContainer()


# EFBC9B FBF3D5
# D6DAC8 - (0.84, 0.85, 0.78, 1) - buttons
# 9CAFAA - background

if __name__ == "__main__":
    gc.set_threshold(2, 2, 2)
    app = MainApp()
    app.run()
