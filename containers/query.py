import random

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput


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
            pos_hint={"x": 0.7, "y": 0.9},
        )
        self.add_widget(self.execute_query_button)
        self.response_label = Label(
            text="",
            size_hint=(1, 0.05),
            pos_hint={"x": 0, "y": 0.85},
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
        label = Label(
            text="Does set of fluents hold at t?",
            halign="left",
            size_hint=(0.88, 0.1),
            pos_hint={"x": 0, "y": 0.6},
        )
        self.add_widget(label)

        time_input = TextInput(
            text="(not) fluent1 (not) fluent2 etc",
            multiline=False,
            size_hint=(0.8, 0.1),
            background_color=(0.84, 0.85, 0.78, 1),
            pos_hint={"x": 0, "y": 0.5},
        )
        self.add_widget(time_input)

        time_input = TextInput(
            text="t",
            multiline=False,
            size_hint=(0.2, 0.1),
            background_color=(0.84, 0.85, 0.78, 1),
            pos_hint={"x": 0.8, "y": 0.5},
        )
        self.add_widget(time_input)

        self.execute_query_button = Button(
            on_release=self._respond_to_query,
            text="Run",
            background_color=(0.84, 0.85, 0.78, 1),
            size_hint=(0.3, 0.1),
            pos_hint={"x": 0.7, "y": 0.4},
        )
        self.add_widget(self.execute_query_button)
        self.response_label = Label(
            text="",
            size_hint=(1, 0.1),
            pos_hint={"x": 0, "y": 0.3},
        )
        self.add_widget(self.response_label)

    def _respond_to_query(self, *args, **kwargs):

        if random.random() <= 0.5:
            response = "No"
        else:
            response = "Yes"
        self.response_label.text = response
