from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput

from containers.input_base import InputContainerBase
from query_resolution.dto import ActionStatement


class ActionsInputContainer(InputContainerBase):

    def __init__(self):
        super().__init__(entry_height=0.05)

    def get_header_label_text(self):
        return "Actions"

    def get_entry_input(self):
        pos_hint = {"y": self.new_entry_y_position, "x": 0}
        input_layout = RelativeLayout(pos_hint=pos_hint)
        input_layout.add_widget(
            TextInput(
                text="A",
                multiline=False,
                size_hint=(0.5, 0.05),
                background_color=(0.84, 0.85, 0.78, 1),
                pos_hint={"x": 0},
            )
        )
        input_layout.add_widget(
            TextInput(
                text="t",
                multiline=False,
                size_hint=(0.5, 0.05),
                background_color=(0.84, 0.85, 0.78, 1),
                pos_hint={"x": 0.5},
            )
        )
        return input_layout

    def get_parsed_entries(self):
        return [
            ActionStatement(
                action=en["input"].children[-1].text,
                time=int(en["input"].children[-2].text),
            )
            for en in self.entry_list
        ]
