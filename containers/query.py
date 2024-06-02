from functools import partial

from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout

from containers.custom_components import TimeInput, time_validation_registry
from containers.input_base import InputContainerBase
from containers.utils import (
    ContradictiveLanguageException,
    parse_fluent_from_string,
)
from query_resolution.algorithms import (
    resolve_condition_query,
    resolve_realizable_query,
)

from .custom_components import (
    ManagedButton,
    ManagedEntryButton,
    ManagedLabel,
    ManagedTextInput,
    default_font_size,
)


class QueryContainer(RelativeLayout):

    def __init__(
        self,
        adl_takes_input,
        adl_causes_input,
        observation_input,
        actions_input,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        time_bound_label = ManagedLabel(
            text="T - upper bound to time",
            size_hint=(1, 0.05),
            pos_hint={"x": 0, "y": 0.95},
        )
        self.add_widget(time_bound_label)
        self.time_bound_input = TimeInput(
            text="",
            multiline=False,
            size_hint=(0.6, 0.05),
            background_color=(0.84, 0.85, 0.78, 1),
            pos_hint={"x": 0.2, "y": 0.9},
        )
        self.add_widget(self.time_bound_input)
        label = ManagedLabel(
            text="Queries",
            size_hint=(1, 0.05),
            pos_hint={"x": 0, "y": 0.85},
        )
        self.add_widget(label)
        self.realizable_query = RealizableQueryBox(
            adl_takes_input,
            adl_causes_input,
            observation_input,
            actions_input,
            self,
        )
        self.add_widget(self.realizable_query)
        self.condition_query = ConditionQueryBox(
            adl_takes_input,
            adl_causes_input,
            observation_input,
            actions_input,
            self,
        )
        self.add_widget(self.condition_query)

    def get_time_bound(self):
        return int(self.time_bound_input.text)


class RealizableQueryBox(RelativeLayout):

    def __init__(
        self,
        adl_takes_input,
        adl_causes_input,
        observation_input,
        actions_input,
        parent,
    ):
        super().__init__()
        label = ManagedLabel(
            text="Is scenario realizable?",
            halign="left",
            size_hint=(0.7, 0.05),
            pos_hint={"x": 0, "y": 0.8},
        )
        self.add_widget(label)
        self.execute_query_button = ManagedButton(
            on_release=self._respond_to_query,
            text="Run",
            background_color=(0.84, 0.85, 0.78, 1),
            size_hint=(0.3, 0.05),
            pos_hint={"x": 0.06, "y": 0.75},
        )
        self.add_widget(self.execute_query_button)
        self.response_label = ManagedLabel(
            text="",
            size_hint=(1, 0.05),
            pos_hint={"x": 0.1, "y": 0.75},
        )
        self.add_widget(self.response_label)

        self.adl_takes_input = adl_takes_input
        self.adl_causes_input = adl_causes_input
        self.observation_input = observation_input
        self.actions_input = actions_input
        self.parent_input = parent

    def _respond_to_query(self, *args, **kwargs):
        if time_validation_registry.all_inputs_are_valid_for_realizable():
            adl_takes_statements = self.adl_takes_input.get_parsed_entries()
            adl_causes_statements = self.adl_causes_input.get_parsed_entries()
            observation_statements = (
                self.observation_input.get_parsed_entries()
            )
            actions_input = self.actions_input.get_parsed_entries()
            time_bound = self.parent_input.get_time_bound()

            try:
                if resolve_realizable_query(
                    adl_takes_statements,
                    adl_causes_statements,
                    observation_statements,
                    actions_input,
                    time_bound,
                )[0]:
                    response = "Yes"
                else:
                    response = "No"
                self.response_label.text = response
            except ContradictiveLanguageException as e:
                create_exception_popup(e)
            except Exception as e:
                e.message = "Unexpected error"
                create_exception_popup(
                    e
                )
        else:
            ex = Exception()
            ex.message = "Invalid input"
            create_exception_popup(
                ex
            )


class ConditionQueryBox(RelativeLayout):

    def __init__(
        self,
        adl_takes_input,
        adl_causes_input,
        observation_input,
        actions_input,
        parent,
    ):
        super().__init__()

        self.entry_height = 0.05

        label = ManagedLabel(
            text="Does set of fluents hold at t?",
            halign="left",
            size_hint=(0.88, 0.1),
            pos_hint={"x": 0, "y": 0.65},
        )
        self.add_widget(label)

        self.execute_query_button = ManagedButton(
            on_release=self._respond_to_query,
            text="Run",
            background_color=(0.84, 0.85, 0.78, 1),
            size_hint=(0.3, 0.05),
            pos_hint={"x": 0.06, "y": 0.62},
        )
        self.add_widget(self.execute_query_button)

        self.response_label = ManagedLabel(
            text="",
            size_hint=(1, 0.05),
            pos_hint={"x": 0.1, "y": 0.62},
        )
        self.add_widget(self.response_label)

        self.time_label = ManagedLabel(
            text="Timepoint",
            halign="left",
            size_hint=(0.26, 0.05),
            pos_hint={"x": 0.06, "y": 0.55},
        )
        self.add_widget(self.time_label)

        self.time_input = TimeInput(
            text="t",
            multiline=False,
            size_hint=(0.5, 0.05),
            background_color=(0.84, 0.85, 0.78, 1),
            pos_hint={"x": 0.36, "y": 0.55},
        )
        self.add_widget(self.time_input)

        self.conditions_label = ManagedLabel(
            text="Fluents",
            size_hint=(0.8, self.entry_height),
            pos_hint={"x": 0, "y": 0.5},
        )
        self.add_widget(self.conditions_label)

        self.add_condition_button = ManagedButton(
            on_release=self._add_condition,
            text="+",
            background_color=(0.84, 0.85, 0.78, 1),
            size_hint=(0.2, self.entry_height),
            pos_hint={"x": 0.8, "y": 0.5},
        )
        self.add_widget(self.add_condition_button)

        self.new_condition_y_position = 0.45
        self.condition_inputs_list = []

        self.adl_takes_input = adl_takes_input
        self.adl_causes_input = adl_causes_input
        self.observation_input = observation_input
        self.actions_input = actions_input
        self.parent_input = parent

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
            ManagedTextInput(
                text="f",
                multiline=False,
                size_hint=(1, 1),
                background_color=(0.84, 0.85, 0.78, 1),
                pos_hint={"x": 0},
            )
        )
        delete_button = ManagedEntryButton(
            on_release=partial(self._delete_entry, entry),
            text="-",
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
        if time_validation_registry.all_inputs_are_valid_for_condition():
            adl_takes_statements = self.adl_takes_input.get_parsed_entries()
            adl_causes_statements = self.adl_causes_input.get_parsed_entries()
            observation_statements = (
                self.observation_input.get_parsed_entries()
            )
            actions_input = self.actions_input.get_parsed_entries()
            fluents_list = self._get_query_fluents_list()
            timepoint = self._get_timepoint()
            time_bound = self.parent_input.get_time_bound()

            try:
                if resolve_condition_query(
                    adl_takes_statements,
                    adl_causes_statements,
                    observation_statements,
                    actions_input,
                    fluents_list,
                    timepoint,
                    time_bound,
                ):
                    response = "Yes"
                else:
                    response = "No"
                self.response_label.text = response
            except ContradictiveLanguageException as e:
                create_exception_popup(e)
            except Exception as e:
                e.message = "Unexpected error"
                create_exception_popup(
                    e
                )
        else:
            ex = Exception()
            ex.message = "Invalid input"
            create_exception_popup(
                ex
            )

    def _get_query_fluents_list(self):
        return [
            parse_fluent_from_string(en["input"].children[-1].text)
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
            ManagedTextInput(
                text="A",
                multiline=False,
                size_hint=(0.5, 0.1),
                background_color=(0.84, 0.85, 0.78, 1),
                pos_hint={"x": 0},
            )
        )
        return input_layout


def create_exception_popup(exception):
    popup = Popup(
        title=type(exception).__name__,
        title_size=default_font_size.val,
        content=ManagedLabel(text=exception.message),
        size_hint=(None, None),
        size=(int(Window.width * 0.4), int(Window.height * 0.4)),
        overlay_color=(0, 0, 0, 0),
    )
    popup.open()