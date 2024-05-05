from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput

from containers.actions import ActionsInputContainer
from containers.adl import AdlCausesInputContainer, AdlTakesInputContainer
from containers.observations import ObservationsInputContainer
from containers.query import QueryContainer


class MainContainer(GridLayout):

    def __init__(self):
        super().__init__()
        self.rows = 1

        adl_layout = GridLayout(rows=2)
        self.adl_takes_input = AdlTakesInputContainer()
        adl_layout.add_widget(self.adl_takes_input)
        self.adl_causes_input = AdlCausesInputContainer()
        adl_layout.add_widget(self.adl_causes_input)
        self.add_widget(
            adl_layout,
        )

        self.observation_input = ObservationsInputContainer()
        self.add_widget(self.observation_input)

        self.actions_input = ActionsInputContainer()
        self.add_widget(self.actions_input)

        self.query = QueryContainer()
        self.add_widget(self.query)


class QueryResponseContainer(BoxLayout):
    def __init__(self):
        super().__init__()
        text_input = TextInput(text="query response", multiline=False)
        self.add_widget(text_input)
