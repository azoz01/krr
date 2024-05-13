from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput

from containers.input_base import InputContainerBase
from containers.input_fields import TimeInput
from containers.utils import parse_fluent_from_string
from query_resolution.dto import ObservationStatement


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
                size_hint=(0.65, 0.05),
                background_color=(0.84, 0.85, 0.78, 1),
                pos_hint={"x": 0},
            )
        )
        input_layout.add_widget(
            TimeInput(
                text="t",
                multiline=False,
                size_hint=(0.25, 0.05),
                background_color=(0.84, 0.85, 0.78, 1),
                pos_hint={"x": 0.65},
            )
        )
        return input_layout

    def get_parsed_entries(self):
        return [
            ObservationStatement(
                fluent=parse_fluent_from_string(en["input"].children[-1].text),
                time=int(en["input"].children[-2].text),
            )
            for en in self.entry_list
        ]
