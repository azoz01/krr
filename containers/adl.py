from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput

from containers.input_base import InputContainerBase


class AdlTakesInputContainer(InputContainerBase):

    def get_header_label_text(self):
        return "ADL - A takes t"

    def get_entry_input(self):
        pos_hint = {"y": self.new_entry_y_position, "x": 0}
        input_layout = RelativeLayout(pos_hint=pos_hint)
        input_layout.add_widget(
            TextInput(
                text="A",
                multiline=False,
                size_hint=(0.5, 0.1),
                background_color=(0.84, 0.85, 0.78, 1),
                pos_hint={"x": 0},
            )
        )
        input_layout.add_widget(
            TextInput(
                text="t",
                multiline=False,
                size_hint=(0.5, 0.1),
                background_color=(0.84, 0.85, 0.78, 1),
                pos_hint={"x": 0.5},
            )
        )
        return input_layout


class AdlCausesInputContainer(InputContainerBase):

    def get_header_label_text(self):
        return "ADL - A causes f if f1, f2, ..."

    def get_entry_input(self):
        pos_hint = {"y": self.new_entry_y_position, "x": 0}
        input_layout = RelativeLayout(pos_hint=pos_hint)
        input_layout.add_widget(
            TextInput(
                text="A",
                multiline=False,
                size_hint=(0.4, 0.1),
                background_color=(0.84, 0.85, 0.78, 1),
                pos_hint={"x": 0},
            )
        )
        input_layout.add_widget(
            TextInput(
                text="t",
                multiline=False,
                size_hint=(0.1, 0.1),
                background_color=(0.84, 0.85, 0.78, 1),
                pos_hint={"x": 0.4},
            )
        )
        input_layout.add_widget(
            TextInput(
                text="f1, f2, ...",
                multiline=False,
                size_hint=(0.5, 0.1),
                background_color=(0.84, 0.85, 0.78, 1),
                pos_hint={"x": 0.5},
            )
        )
        return input_layout
