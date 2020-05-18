import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QDialog
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QScrollArea, QPlainTextEdit
from PyQt5.QtWidgets import QDesktopWidget, QMenu, QAction
from PyQt5.QtGui import QIcon, QPixmap

class QLoadMVADialog(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.left = 100
        self.top = 100
        self.height = 300
        self.width = 300
        self.title = "Load MVA"
        self.initUI()
        self.parent = parent

    def initUI(self):
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        VBoxLayout = QVBoxLayout()

        HBoxLayout = QHBoxLayout()
        self.mva_text = QPlainTextEdit()
        # self.mva_text.setStyleSheet("font: 24px;")
        HBoxLayout.addWidget(self.mva_text)

        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")
        save_btn.clicked.connect(self.saveSettings)
        cancel_btn.clicked.connect(self.cancelSettings)
        confirm_HBoxLayout = QHBoxLayout()
        confirm_HBoxLayout.addStretch()
        confirm_HBoxLayout.addWidget(save_btn)
        confirm_HBoxLayout.addWidget(cancel_btn)

        VBoxLayout.addLayout(HBoxLayout)
        VBoxLayout.addLayout(confirm_HBoxLayout)
        self.setLayout(VBoxLayout)

    def saveSettings(self):
        self.parent.setLoadedMVAText(self.mva_text.toPlainText())
        self.accept()
        return

    def cancelSettings(self):
        self.reject()
        return

    def exec_(self):
        self.mva_text.setPlainText(self.parent.loaded_mva_text)
        super().exec_()