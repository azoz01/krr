import random
from functools import partial

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput

from containers.input_base import InputContainerBase


class QueryContainer(RelativeLayout):
    def __init__(self):
        super().__init__()
        label = Label(
            text="Queries",
            size_hint=(1, 0.05),
            pos_hint={"x": 0, "y": 0.95},
        )
        self.add_widget(label)
        self.realizable_query = RealizableQueryBox()
        self.add_widget(self.realizable_query)
        self.condition_query = ConditionQueryBox()
        self.add_widget(self.condition_query)


class RealizableQueryBox(RelativeLayout):
    def __init__(self):
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
            # font_size=,
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

    def _respond_to_query(self, *args, **kwargs):
        if random.random() <= 0.5:
            response = "No"
        else:
            response = "Yes"
        self.response_label.text = response


class ConditionQueryBox(RelativeLayout):
    def __init__(self):
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
        self.condition_list = []

    def _add_condition(self, *args, **kwargs):
        if self.new_condition_y_position < -0.0001:
            return
        entry_id = len(self.condition_list)
        entry = dict()
        input = TextInput(
            text="f",
            multiline=False,
            size_hint=(0.9, self.entry_height),
            background_color=(0.84, 0.85, 0.78, 1),
            pos_hint={"x": 0, "y": self.new_condition_y_position},
        )
        delete_button = Button(
            on_release=partial(self._delete_entry, entry),
            text="-",
            font_size=22,
            background_color=(0.84, 0.85, 0.78, 1),
            size_hint=(0.1, self.entry_height),
            pos_hint={"x": 0.9, "y": self.new_condition_y_position},
        )
        entry.update({"id": entry_id, "input": input, "delete": delete_button})
        self.condition_list.append(entry)
        self.add_widget(input)
        self.add_widget(delete_button)
        self.new_condition_y_position -= self.entry_height

    def _delete_entry(self, entry, *args, **kwargs):
        entry_id = entry["id"]
        deleted_entry = self.condition_list.pop(entry_id)
        self.remove_widget(deleted_entry["input"])
        self.remove_widget(deleted_entry["delete"])
        for i in range(entry_id, len(self.condition_list)):
            entry = self.condition_list[i]
            entry["id"] -= 1
            entry["input"].pos_hint["y"] += self.entry_height
            entry["delete"].pos_hint["y"] += self.entry_height
        self.new_condition_y_position += self.entry_height

    def _respond_to_query(self, *args, **kwargs):
        if random.random() <= 0.5:
            response = "No"
        else:
            response = "Yes"
        self.response_label.text = response


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
