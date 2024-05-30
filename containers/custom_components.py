from copy import deepcopy

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from containers.utils import GlobalValueHolder

managed_fields = []
default_font_size = GlobalValueHolder(15)


class ManagedTextInput(TextInput):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        managed_fields.append(self)
        self.font_size = default_font_size.val


class ManagedLabel(Label):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        managed_fields.append(self)
        self.font_size = default_font_size.val


class ManagedButton(Button):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        managed_fields.append(self)
        self.font_size = default_font_size.val


class ManagedEntryButton(Button):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cleanup_callback = kwargs.get("on_release", lambda x: None)
        managed_fields.append(self)
        self.font_size = default_font_size.val

    def delete(self):
        self.cleanup_callback()
        managed_fields.pop(managed_fields.index(self))


class TimeValidationRegistry:
    def __init__(self):
        self.valid_inputs_indicators = []

    def register_function(self, function):
        self.valid_inputs_indicators.append(False)
        index_to_modify = len(self.valid_inputs_indicators) - 1

        def monitored_function(*args, **kwargs):
            output = function(*args, **kwargs)
            self.valid_inputs_indicators[index_to_modify] = output
            return output

        return index_to_modify, monitored_function

    def all_inputs_are_valid_for_condition(self):
        return all(self.valid_inputs_indicators)

    def all_inputs_are_valid_for_realizable(self):
        temp = deepcopy(self.valid_inputs_indicators)
        temp.pop(1)
        return all(temp)


time_validation_registry = TimeValidationRegistry()


class TimeInput(ManagedTextInput):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_color = self.background_color
        self.registry_index, self.is_input_valid = (
            time_validation_registry.register_function(self.is_input_valid)
        )

    def on_focus(self, instance, value):
        input = self.text
        if not value and not self.is_input_valid(input):
            self.background_color = "#FF0000"
        if not value and self.is_input_valid(input):
            self.background_color = self.default_color

    def is_input_valid(self, input):
        try:
            return int(input) >= 0
        except ValueError:
            return False

    def cleanup(self):
        time_validation_registry.valid_inputs_indicators[
            self.registry_index
        ] = True
