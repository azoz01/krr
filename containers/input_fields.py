from kivy.uix.textinput import TextInput


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

        return monitored_function

    def all_inputs_are_valid_for_condition(self):
        return all(self.valid_inputs_indicators)

    def all_inputs_are_valid_for_realizable(self):
        return all(self.valid_inputs_indicators[1:])


time_validation_registry = TimeValidationRegistry()


class TimeInput(TextInput):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_color = self.background_color
        self.is_input_valid = time_validation_registry.register_function(
            self.is_input_valid
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
