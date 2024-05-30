from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout

from containers.actions import ActionsInputContainer
from containers.adl import AdlCausesInputContainer, AdlTakesInputContainer
from containers.custom_components import ManagedTextInput
from containers.observations import ObservationsInputContainer
from containers.query import QueryContainer
from containers.utils_buttons import UtilsButtons


class MainContainer(RelativeLayout):

    def __init__(self):
        super().__init__()

        utils_buttons = UtilsButtons(
            main_container=self,
            size_hint=(1, 0.05),
            pos_hint={"x": 0.0, "y": 0.95},
        )
        self.add_widget(utils_buttons)

        adl_layout = GridLayout(
            rows=2, pos_hint={"x": 0.0, "y": 0.05}, size_hint=(0.25, 0.9)
        )
        self.adl_takes_input = AdlTakesInputContainer()
        adl_layout.add_widget(self.adl_takes_input)
        self.adl_causes_input = AdlCausesInputContainer()
        adl_layout.add_widget(self.adl_causes_input)
        self.add_widget(
            adl_layout,
        )

        self.observation_input = ObservationsInputContainer(
            pos_hint={"x": 0.25, "y": 0.05}, size_hint=(0.25, 0.9)
        )
        self.add_widget(self.observation_input)

        self.actions_input = ActionsInputContainer(
            pos_hint={"x": 0.5, "y": 0.05}, size_hint=(0.25, 0.9)
        )
        self.add_widget(self.actions_input)

        self.query = QueryContainer(
            self.adl_takes_input,
            self.adl_causes_input,
            self.observation_input,
            self.actions_input,
            pos_hint={"x": 0.75, "y": 0.05},
            size_hint=(0.25, 0.9),
        )
        self.add_widget(self.query)


class QueryResponseContainer(BoxLayout):
    def __init__(self):
        super().__init__()
        text_input = ManagedTextInput(text="query response", multiline=False)
        self.add_widget(text_input)
