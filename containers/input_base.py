from functools import partial

from kivy.uix.relativelayout import RelativeLayout

from containers.custom_components import (
    ManagedButton,
    ManagedEntryButton,
    ManagedLabel,
    TimeInput,
)


class InputContainerBase(RelativeLayout):
    def __init__(self, entry_height=0.1, header=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.entry_height = entry_height
        self._initialize_layout()
        if header:
            self._initialize_header()
        self._initialize_buttons()
        self.entry_list = []
        self.new_entry_y_position = 1 - 2 * self.entry_height

    def get_header_label_text(self):
        raise NotImplementedError("Not implemented")

    def get_entry_input(self):
        raise NotImplementedError("Not implemented")

    def get_parsed_entries(self):
        raise NotImplementedError("Not implemented")

    def _initialize_layout(self):
        with self.canvas.before:
            self.border_color = (0, 0, 0, 0)

    def _initialize_header(self):
        label = ManagedLabel(
            text=self.get_header_label_text(),
            size_hint=(0.8, self.entry_height),
            pos_hint={"x": 0, "y": 1 - self.entry_height},
        )
        self.add_widget(label)

    def _initialize_buttons(self):
        add_entry_button = ManagedButton(
            on_release=self._add_entry,
            text="+",
            background_color=(0.84, 0.85, 0.78, 1),
            size_hint=(0.2, self.entry_height),
            pos_hint={"x": 0.8, "y": 1 - self.entry_height},
        )
        self.add_widget(add_entry_button)

    def _add_entry(self, *args, **kwargs):
        if self.new_entry_y_position < -0.01:
            return
        entry_id = len(self.entry_list)
        entry = dict()
        input = self.get_entry_input()
        delete_button = ManagedEntryButton(
            on_release=partial(self._delete_entry, entry),
            text="-",
            background_color=(0.84, 0.85, 0.78, 1),
            size_hint=(0.1, self.entry_height),
            pos_hint={"x": 0.9, "y": self.new_entry_y_position},
        )
        entry.update({"id": entry_id, "input": input, "delete": delete_button})
        self.entry_list.append(entry)
        self.add_widget(input)
        self.add_widget(delete_button)
        self.new_entry_y_position -= self.entry_height

    def _delete_entry(self, entry, *args, **kwargs):
        entry_id = entry["id"]
        deleted_entry = self.entry_list.pop(entry_id)
        self.remove_widget(deleted_entry["input"])
        self.remove_widget(deleted_entry["delete"])
        for child in deleted_entry["input"].children:
            if isinstance(child, TimeInput):
                child.cleanup()
        for i in range(entry_id, len(self.entry_list)):
            entry = self.entry_list[i]
            entry["id"] -= 1
            entry["input"].pos_hint["y"] += self.entry_height
            entry["delete"].pos_hint["y"] += self.entry_height
        self.new_entry_y_position += self.entry_height
        del deleted_entry["input"]
