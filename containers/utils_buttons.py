from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout

from .custom_components import (
    ManagedButton,
    ManagedEntryButton,
    ManagedLabel,
    ManagedTextInput,
    default_font_size,
    managed_fields,
)
from .utils import HELP_TEXT


class UtilsButtons(RelativeLayout):

    def __init__(self, main_container, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_container = main_container
        help_button = ManagedButton(
            on_release=create_help_popup,
            text="Help",
            size_hint=(0.1, 1),
            pos_hint={"x": 0.0, "y": 0.0},
        )
        self.add_widget(help_button)

        clear_all_button = ManagedButton(
            on_release=clear_all_inputs,
            text="Clear all",
            size_hint=(0.1, 1),
            pos_hint={"x": 0.1, "y": 0.0},
        )
        self.add_widget(clear_all_button)

        increase_font_button = ManagedButton(
            on_release=increment_font_size,
            text="Increase font size",
            size_hint=(0.1, 1),
            pos_hint={"x": 0.2, "y": 0.0},
        )
        self.add_widget(increase_font_button)

        decrease_font_button = ManagedButton(
            on_release=decrement_font_size,
            text="Decrease font size",
            size_hint=(0.1, 1),
            pos_hint={"x": 0.3, "y": 0.0},
        )
        self.add_widget(decrease_font_button)


def increment_font_size(*args, **kwargs):
    for field in managed_fields:
        field.font_size += 1
    global default_font_size
    default_font_size.val += 1


def decrement_font_size(*args, **kwargs):
    for field in managed_fields:
        field.font_size -= 1
    global default_font_size
    default_font_size.val -= 1


def clear_all_inputs(*args, **kwargs):
    for field in managed_fields:
        if isinstance(field, ManagedEntryButton):
            field.delete()
        if isinstance(field, ManagedTextInput):
            field.text = ""


def create_help_popup(*args, **kwargs):
    popup = Popup(
        title="Help",
        title_size=default_font_size.val,
        content=ManagedLabel(text=HELP_TEXT),
        size_hint=(None, None),
        size=(int(Window.width * 0.7), int(Window.height * 0.95)),
        overlay_color=(0, 0, 0, 0),
    )
    popup.open()
