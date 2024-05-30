import re

from kivy.uix.relativelayout import RelativeLayout

from containers.custom_components import TimeInput
from containers.input_base import InputContainerBase
from containers.utils import parse_fluent_from_string
from query_resolution.dto import AdlCausesStatement, AdlTakesStatement

from .custom_components import ManagedTextInput


class AdlTakesInputContainer(InputContainerBase):

    def get_header_label_text(self):
        return "ADL - A takes t"

    def get_entry_input(self):
        pos_hint = {"y": self.new_entry_y_position, "x": 0}
        input_layout = RelativeLayout(pos_hint=pos_hint)
        input_layout.add_widget(
            ManagedTextInput(
                text="A",
                multiline=False,
                size_hint=(0.5, 0.1),
                background_color=(0.84, 0.85, 0.78, 1),
                pos_hint={"x": 0},
            )
        )
        input_layout.add_widget(
            TimeInput(
                text="t",
                multiline=False,
                size_hint=(0.5, 0.1),
                background_color=(0.84, 0.85, 0.78, 1),
                pos_hint={"x": 0.5},
            )
        )
        return input_layout

    def get_parsed_entries(self):
        return [
            AdlTakesStatement(
                action=en["input"].children[-1].text,
                time=int(en["input"].children[-2].text),
            )
            for en in self.entry_list
        ]


class AdlCausesInputContainer(InputContainerBase):

    def get_header_label_text(self):
        return "ADL - A causes f if f1, f2, ..."

    def get_entry_input(self):
        pos_hint = {"y": self.new_entry_y_position, "x": 0}
        input_layout = RelativeLayout(pos_hint=pos_hint)
        input_layout.add_widget(
            ManagedTextInput(
                text="A",
                multiline=False,
                size_hint=(0.25, 0.1),
                background_color=(0.84, 0.85, 0.78, 1),
                pos_hint={"x": 0},
            )
        )
        input_layout.add_widget(
            ManagedTextInput(
                text="f",
                multiline=False,
                size_hint=(0.25, 0.1),
                background_color=(0.84, 0.85, 0.78, 1),
                pos_hint={"x": 0.25},
            )
        )
        input_layout.add_widget(
            ManagedTextInput(
                text="f1, f2, ...",
                multiline=False,
                size_hint=(0.5, 0.1),
                background_color=(0.84, 0.85, 0.78, 1),
                pos_hint={"x": 0.5},
            )
        )
        return input_layout

    def get_parsed_entries(self):
        return [
            AdlCausesStatement(
                action=en["input"].children[-1].text,
                fluent=parse_fluent_from_string(en["input"].children[-2].text),
                condition_fluents=[
                    parse_fluent_from_string(s)
                    for s in re.sub(
                        r"\s+", " ", en["input"].children[-3].text
                    ).split(",")
                ],
            )
            for en in self.entry_list
        ]
