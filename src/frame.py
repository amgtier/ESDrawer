from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QPlainTextEdit, QPushButton, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from photo_viewer import QPhotoViewer

class QMainFrame(QWidget):
    def __init__(self, MainWindow):
        super().__init__()

        self.prefix = "RCTP_MVA"
        self.add_mode = "line"

        self.MainWindow = MainWindow
        self.widget = self.MainWidget()

        self._zoom = 0

    def MainWidget(self):
        width = self.MainWindow.width
        height = self.MainWindow.height

        self.background = QPhotoViewer(self)

        EditorLayout = QVBoxLayout()

        self.new_mva_lines = QPlainTextEdit()
        self.edit_prefix = QLineEdit()
        label_prefix = QLabel("Label: ")
        label_prefix.setFixedWidth(40)
        self.toggle_line = QPushButton("Line")
        self.toggle_text = QPushButton("Text")
        self.edit_prefix.setText(self.prefix)
        self.edit_prefix.setFixedWidth(150)
        self.edit_prefix.textChanged.connect(self.changePrefix)
        self.new_mva_lines.textChanged.connect(self.background.newMvaChanged)
        self.toggle_line.setCheckable(True)
        self.toggle_text.setCheckable(True)

        self.toggle_line.setChecked(True)
        self.toggle_text.setChecked(False)

        self.toggle_text.clicked.connect(self.setText)
        self.toggle_line.clicked.connect(self.setLine)
        # save_btn = QPushButton("Save")
        # save_btn.setDisabled(True)

        HBoxLayout = QHBoxLayout()
        # HBoxLayout.addWidget(save_btn)
        HBoxLayout.addWidget(label_prefix)
        HBoxLayout.addWidget(self.edit_prefix)
        HBoxLayout.addWidget(self.toggle_line)
        HBoxLayout.addWidget(self.toggle_text)
        HBoxLayout.addWidget(QLabel())

        EditorLayout.addLayout(HBoxLayout)
        EditorLayout.addWidget(self.new_mva_lines)

        VBoxLayout = QVBoxLayout()
        VBoxLayout.addWidget(self.background, 1)
        VBoxLayout.addLayout(EditorLayout)

        widget = QWidget()
        widget.setLayout(VBoxLayout)
        return widget

    def setBackgroundPath(self, path: "str"):
        self.background.setPhotoPath(path)

    def changePrefix(self, txt):
        if len(txt) == 0:
            self.edit_prefix.setText(self.prefix[0])
        if txt and self.prefix:
            org_mva_lines = self.new_mva_lines.toPlainText()
            self.new_mva_lines.setPlainText(org_mva_lines.replace(self.prefix, txt))
            self.prefix = txt

    def setLine(self):
        self.add_mode = "line"
        self.toggle_line.setChecked(True)
        self.toggle_text.setChecked(False)

    def setText(self):
        self.add_mode = "text"
        self.toggle_line.setChecked(False)
        self.toggle_text.setChecked(True)
