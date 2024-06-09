from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QScrollArea, QSizePolicy
import json

from graph_handler import GraphHandler


window = None

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Social Robot Design - Behaviour Tool")

        self.gh = GraphHandler()

        questions_file = open("questions.json")
        self.questions = json.load(questions_file)
        questions_file.close()

        self.current_question = self.questions["vision"]

        self.question_widget = QuestionWidget(self.gh, self.current_question)
        self.question_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.image_label = QLabel()
        #self.image_label.setPixmap(QPixmap("graph.png"))

        self.image_scroll_area = QScrollArea()
        self.image_scroll_area.setWidget(self.image_label)
        self.image_scroll_area.setWidgetResizable(True)
        self.image_scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout = QHBoxLayout()
        layout.addWidget(self.question_widget)
        layout.addWidget(self.image_scroll_area)

        self.setLayout(layout)


    def update_window(self, next_question):
        self.image_label.setPixmap(QPixmap("graph.png"))

        self.current_question = self.questions[next_question]
        self.question_widget.question = self.current_question
        self.question_widget.question_label.setText(self.current_question["question"])


class QuestionWidget(QWidget):
    def __init__(self, gh, question):
        super().__init__()

        self.gh = gh
        self.question = question

        self.question_label = QLabel(question["question"])
        self.question_label.setWordWrap(True)
        self.question_label.setMaximumWidth(150)
        self.question_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        yes_button = QPushButton("Yes")
        yes_button.clicked.connect(lambda: self.submit_button(True))
        no_button = QPushButton("No")
        no_button.clicked.connect(lambda: self.submit_button(False))

        button_layout = QHBoxLayout()
        button_layout.addWidget(yes_button)
        button_layout.addWidget(no_button)

        layout = QVBoxLayout()
        layout.addWidget(self.question_label)
        layout.addLayout(button_layout)

        self.setLayout(layout)


    def submit_button(self, answered_yes : bool):
        if answered_yes:
            nodes = self.question["yes_nodes"]
            next_question = self.question["yes_next_question"]
        else:
            nodes = self.question["no_nodes"]
            next_question = self.question["no_next_question"]
        self.gh.add_connection(nodes)
        self.gh.save_graph_png()

        self.parentWidget().update_window(next_question)



if __name__ == "__main__":
    app = QApplication()

    window = MainWindow()
    window.show()

    app.exec()