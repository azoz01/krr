from functools import partial

from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput

from containers.input_base import InputContainerBase
from query_resolution.algorithms import (
    resolve_condition_query,
    resolve_realizable_query,
)
from query_resolution.dto import QueryFluent


class QueryContainer(RelativeLayout):

    def __init__(
        self,
        adl_takes_input,
        adl_causes_input,
        observation_input,
        actions_input,
    ):
        super().__init__()
        label = Label(
            text="Queries",
            size_hint=(1, 0.05),
            pos_hint={"x": 0, "y": 0.95},
        )
        self.add_widget(label)
        self.realizable_query = RealizableQueryBox(
            adl_takes_input,
            adl_causes_input,
            observation_input,
            actions_input,
        )
        self.add_widget(self.realizable_query)
        self.condition_query = ConditionQueryBox(
            adl_takes_input,
            adl_causes_input,
            observation_input,
            actions_input,
        )
        self.add_widget(self.condition_query)


class RealizableQueryBox(RelativeLayout):

    def __init__(
        self,
        adl_takes_input,
        adl_causes_input,
        observation_input,
        actions_input,
    ):
        super().__init__()
        label = Label(
            text="Is scenario realizable?",
            halign="left",
            size_hint=(0.7, 0.05),
            pos_hint={"x": 0, "y": 0.9},
        )
        self.add_widget(label)
        self.execute_query_button = Button(
            on_release=self._respond_to_query,
            text="Run",
            background_color=(0.84, 0.85, 0.78, 1),
            size_hint=(0.3, 0.05),
            pos_hint={"x": 0.06, "y": 0.85},
        )
        self.add_widget(self.execute_query_button)
        self.response_label = Label(
            text="",
            size_hint=(1, 0.05),
            pos_hint={"x": 0.1, "y": 0.85},
        )
        self.add_widget(self.response_label)

        self.adl_takes_input = adl_takes_input
        self.adl_causes_input = adl_causes_input
        self.observation_input = observation_input
        self.actions_input = actions_input

    def _respond_to_query(self, *args, **kwargs):
        adl_takes_statements = self.adl_takes_input.get_parsed_entries()
        adl_causes_statements = self.adl_causes_input.get_parsed_entries()
        observation_statements = self.observation_input.get_parsed_entries()
        actions_input = self.actions_input.get_parsed_entries()

        if resolve_realizable_query(
            adl_takes_statements,
            adl_causes_statements,
            observation_statements,
            actions_input,
        ):
            response = "No"
        else:
            response = "Yes"
        self.response_label.text = response


class ConditionQueryBox(RelativeLayout):

    def __init__(
        self,
        adl_takes_input,
        adl_causes_input,
        observation_input,
        actions_input,
    ):
        super().__init__()

        self.entry_height = 0.05

        label = Label(
            text="Does set of fluents hold at t?",
            halign="left",
            size_hint=(0.88, 0.1),
            pos_hint={"x": 0, "y": 0.75},
        )
        self.add_widget(label)

        self.execute_query_button = Button(
            on_release=self._respond_to_query,
            text="Run",
            background_color=(0.84, 0.85, 0.78, 1),
            size_hint=(0.3, 0.05),
            pos_hint={"x": 0.06, "y": 0.72},
        )
        self.add_widget(self.execute_query_button)

        self.response_label = Label(
            text="",
            size_hint=(1, 0.05),
            pos_hint={"x": 0.1, "y": 0.72},
        )
        self.add_widget(self.response_label)

        self.time_label = Label(
            text="Timepoint",
            halign="left",
            size_hint=(0.26, 0.05),
            pos_hint={"x": 0.06, "y": 0.65},
        )
        self.add_widget(self.time_label)

        self.time_input = TextInput(
            text="t",
            multiline=False,
            size_hint=(0.5, 0.05),
            background_color=(0.84, 0.85, 0.78, 1),
            pos_hint={"x": 0.36, "y": 0.65},
        )
        self.add_widget(self.time_input)

        self.conditions_label = Label(
            text="Fluents",
            size_hint=(0.8, self.entry_height),
            pos_hint={"x": 0, "y": 0.6},
        )
        self.add_widget(self.conditions_label)

        self.add_condition_button = Button(
            on_release=self._add_condition,
            text="+",
            font_size=22,
            background_color=(0.84, 0.85, 0.78, 1),
            size_hint=(0.2, self.entry_height),
            pos_hint={"x": 0.8, "y": 0.6},
        )
        self.add_widget(self.add_condition_button)

        self.new_condition_y_position = 0.55
        self.condition_inputs_list = []

        self.adl_takes_input = adl_takes_input
        self.adl_causes_input = adl_causes_input
        self.observation_input = observation_input
        self.actions_input = actions_input

    def _add_condition(self, *args, **kwargs):
        if self.new_condition_y_position < -0.0001:
            return
        entry_id = len(self.condition_inputs_list)
        entry = dict()

        input_layout = RelativeLayout(
            pos_hint={"x": 0, "y": self.new_condition_y_position},
            size_hint=(0.9, self.entry_height),
        )
        input_layout.add_widget(
            TextInput(
                text="f",
                multiline=False,
                size_hint=(0.55, 1),
                background_color=(0.84, 0.85, 0.78, 1),
                pos_hint={"x": 0},
            )
        )
        input_layout.add_widget(
            CheckBox(
                size_hint=(0.05, 1),
                pos_hint={"x": 0.6},
            )
        )
        input_layout.add_widget(
            Label(
                text="negate",
                pos_hint={"x": 0.75, "y": 0.5},
                size_hint=(0.05, 0.1),
            )
        )
        delete_button = Button(
            on_release=partial(self._delete_entry, entry),
            text="-",
            font_size=22,
            background_color=(0.84, 0.85, 0.78, 1),
            size_hint=(0.1, self.entry_height),
            pos_hint={"x": 0.9, "y": self.new_condition_y_position},
        )
        entry.update(
            {"id": entry_id, "input": input_layout, "delete": delete_button}
        )
        self.condition_inputs_list.append(entry)
        self.add_widget(input_layout)
        self.add_widget(delete_button)
        self.new_condition_y_position -= self.entry_height

    def _delete_entry(self, entry, *args, **kwargs):
        entry_id = entry["id"]
        deleted_entry = self.condition_inputs_list.pop(entry_id)
        self.remove_widget(deleted_entry["input"])
        self.remove_widget(deleted_entry["delete"])
        for i in range(entry_id, len(self.condition_inputs_list)):
            entry = self.condition_inputs_list[i]
            entry["id"] -= 1
            entry["input"].pos_hint["y"] += self.entry_height
            entry["delete"].pos_hint["y"] += self.entry_height
        self.new_condition_y_position += self.entry_height

    def _respond_to_query(self, *args, **kwargs):
        adl_takes_statements = self.adl_takes_input.get_parsed_entries()
        adl_causes_statements = self.adl_causes_input.get_parsed_entries()
        observation_statements = self.observation_input.get_parsed_entries()
        actions_input = self.actions_input.get_parsed_entries()
        fluents_list = self._get_query_fluents_list()
        timepoint = self._get_timepoint()

        if resolve_condition_query(
            adl_takes_statements,
            adl_causes_statements,
            observation_statements,
            actions_input,
            fluents_list,
            timepoint,
        ):
            response = "No"
        else:
            response = "Yes"
        self.response_label.text = response

    def _get_query_fluents_list(self):
        return [
            QueryFluent(
                fluent=en["input"].children[-1].text,
                negated=en["input"].children[-2].active,
            )
            for en in self.condition_inputs_list
        ]

    def _get_timepoint(self):
        return int(self.time_input.text)


class ConditionsInput(InputContainerBase):

    def get_header_label_text(self):
        return "Fluents"

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
        return input_layout
