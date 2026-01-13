from PySide6.QtWidgets import QApplication as Application
from PySide6.QtWidgets import QMainWindow, QWidget
from PySide6.QtGui import QColor
from the_data_clasification_interface import Ui_MainWindow
from conversation_page import Ui_page
from data_loading import DataProvider
import numpy as np


class ConversationPage(QWidget, Ui_page):
    """Purpose: This class represents a single "page" of conversation history (displaying 4 messages at a time).
    It handles the display of text, the assignment of colors to characters,
    and most importantly,the tracking of user inputs via sliders.
    """

    def __init__(self, messages, values, colors):
        super().__init__()
        self.setupUi(self)
        self.is_modified = False
        self.labels = [self.text_1, self.text_2, self.text_3, self.text_4]
        self.connotations = [
            self.connotation_1,
            self.connotation_2,
            self.connotation_3,
            self.connotation_4,
        ]
        self.containers = [
            self.message_1,
            self.message_2,
            self.message_3,
            self.message_4,
        ]
        for slider in self.connotations:
            slider.setMinimum(-10)
            slider.setMaximum(10)
            slider.setValue(0)
            slider.setTickPosition(slider.TickPosition.TicksBelow)
        for i in range(4):
            if i < len(messages):
                self.labels[i].setText(messages[i])
                self.labels[i].setWordWrap(True)
                color_hex = colors[i].name()
                self.containers[i].setStyleSheet(f"background-color: {color_hex};")
                self.connotations[i].setValue(values[i])
            else:
                self.containers[i].hide()
        self.changed = np.zeros(4, dtype=bool)
        for i in range(len(self.connotations)):
            self.connotations[i].valueChanged.connect(
                lambda val, i=i: self.on_value_change(i)
            )

        def on_value_change(self, i):
            self.is_modified = True
            self.changed[i] = True


class DataClassificationApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Data Classification Interface")
        self.the_top_holder.hide()
        self.collapse_button.clicked.connect(self.toggle_diss_menu)
        self.provider = DataProvider()
        self.load_discussions()
        self.colors = [
            QColor(220, 240, 255),
            QColor(230, 255, 230),
            QColor(240, 230, 255),
            QColor(255, 235, 220),
        ]
        self.disscussions_list.clicked.connect(self.diss_list_clicked)
        self.next.clicked.connect(self.conversation_next)
        self.previous.clicked.connect(self.conversation_previous)
        self.save.clicked.connect(self.save_current)
        self.close.clicked.connect(self.clean_diss_space)

    def collapse_diss_menu(self):
        self.title.hide()
        self.disscussions_list.hide()
        self.the_top_holder.show()
        self.main_horizantal_layout.setStretch(1, 20)

    def clean_diss_space(self):
        self.provider.data_stat.to_csv(
            "./data_set/data_stat.tsv", sep="\t", index=False
        )
        while self.conversation_space.count() > 0:
            widget = self.conversation_space.widget(0)
            self.conversation_space.removeWidget(widget)
            widget.deleteLater()

    def load_conversation(self, diss_ID):
        self.clean_diss_space()
        data = self.provider.get_conversation(diss_ID, True)
        unique = list(set(data["character_id"]))
        colors_dict = {unique[i]: self.colors[i] for i in range(len(unique))}
        for i in range(0, len(data), 4):
            chunk = data.iloc[i : i + 4]
            messages = chunk["text"].values
            values = chunk["connotation"].values
            people = chunk["character_id"].values
            colors = [colors_dict[person] for person in people]
            values[np.isnan(values)] = 0
            self.conversation_space.addWidget(
                ConversationPage(messages, values, colors)
            )
        self.conversation_space.setCurrentIndex(0)

    def diss_list_clicked(self, row_index):
        self.save_current()
        self.load_conversation(row_index.row() + 1)

    def load_discussions(self):
        self.disscussions_list.setUpdatesEnabled(False)
        self.disscussions_list.clear()
        ids = self.provider.data_stat["id"].values.astype(int)
        lengths = self.provider.data_stat["disscussion_length"].values.astype(int)
        done = self.provider.data_stat["is_complete"].values.astype(int)
        labels = [
            f"conv{ids[i]}: {lengths[i]} Lines | done {done[i]}/{lengths[i]}"
            for i in range(len(ids))
        ]
        self.disscussions_list.addItems(labels)
        for i in range(len(ids)):
            if lengths[i] == done[i]:
                item = self.disscussions_list.item(i)
                item.setBackground(QColor(200, 230, 201))
            elif done[i] > 0:
                item = self.disscussions_list.item(i)
                item.setBackground(QColor(231, 230, 201))
        self.disscussions_list.setUpdatesEnabled(True)

    def save_current(self):
        if self.conversation_space.count() == 0:
            return
        index = self.conversation_space.currentIndex()
        page = self.conversation_space.widget(index)
        if not page.is_modified:
            return
        conversation_id = self.disscussions_list.currentIndex().row() + 1
        i = 0
        for scaler in page.connotations:
            if not page.changed[i]:
                i += 1
                continue
            self.provider.update_connotation(
                conversation_id, index * 4 + i, scaler.value()
            )
            i += 1
        page.changed.fill(False)
        item = self.disscussions_list.item(conversation_id - 1)
        length = int(
            self.provider.data_stat["disscussion_length"].values[conversation_id - 1]
        )
        done = int(self.provider.data_stat["is_complete"].values[conversation_id - 1])
        item.setText(f"conv{conversation_id}: {length} Lines | done {done}/{length}")
        if done == length:
            item.setBackground(QColor(200, 230, 201))
        else:
            item.setBackground(QColor(231, 230, 201))
        page.is_modified = False

    def conversation_next(self):
        self.save_current()
        index = self.conversation_space.currentIndex()
        if index < self.conversation_space.count() - 1:
            self.conversation_space.setCurrentIndex(index + 1)

    def conversation_previous(self):
        self.save_current()
        index = self.conversation_space.currentIndex()
        if index > 0:
            self.conversation_space.setCurrentIndex(index - 1)

    def expand_diss_menu(self):
        self.title.show()
        self.disscussions_list.show()
        self.the_top_holder.hide()
        self.main_horizantal_layout.setStretch(1, 5)

    def toggle_diss_menu(self):
        if self.disscussions_list.isVisible():
            self.collapse_diss_menu()
        else:
            self.expand_diss_menu()


if __name__ == "__main__":
    app = Application([])
    window = DataClassificationApp()
    window.show()
    app.exec()
