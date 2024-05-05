from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput

from containers.input_base import InputContainerBase


class ObservationsInputContainer(InputContainerBase):

    def __init__(self):
        super().__init__(entry_height=0.05)

    def get_header_label_text(self):
        return "Observations"

    def get_entry_input(self):
        pos_hint = {"y": self.new_entry_y_position, "x": 0}
        input_layout = RelativeLayout(pos_hint=pos_hint)
        input_layout.add_widget(
            TextInput(
                text="f",
                multiline=False,
                size_hint=(0.4, 0.05),
                background_color=(0.84, 0.85, 0.78, 1),
                pos_hint={"x": 0},
            )
        )
        input_layout.add_widget(
            TextInput(
                text="t",
                multiline=False,
                size_hint=(0.15, 0.05),
                background_color=(0.84, 0.85, 0.78, 1),
                pos_hint={"x": 0.4},
            )
        )
        input_layout.add_widget(
            CheckBox(
                size_hint=(0.05, 0.05),
                pos_hint={"x": 0.6},
            )
        )
        input_layout.add_widget(
            Label(
                text="negate",
                pos_hint={"x": 0.75, "y": -0.022},
                size_hint=(0.05, 0.1),
            )
        )
        return input_layout
