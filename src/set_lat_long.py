import sys
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtWidgets import QApplication, QWidget, QDialog
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QScrollArea, QLabel, QLineEdit
from PyQt5.QtWidgets import QDesktopWidget, QMenu, QAction
from PyQt5.QtGui import QIcon, QPixmap, QRegExpValidator

class QSetLatLong(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.left = 100
        self.top = 100
        # self.height = 300
        # self.width = 300
        self.title = "Set Latitude/ Longitude"
        self.parent = parent
        self.initUI()

    def initUI(self):
        # self.setGeometry(self.left, self.top, self.width, self.height)
        # self.setGeometry(self.left, self.top)
        regexp_lat = QRegExp(r"^([NnSs]0(\d{2}).(\d{2})(.(\d{2}))?(.(\d{3}))?)$")
        regexp_long = QRegExp(r"^([EeWw][01](\d{2}).(\d{2})(.(\d{2}))?(.(\d{3}))?)$")
        valid_lat = QRegExpValidator(regexp_lat)
        valid_long = QRegExpValidator(regexp_long)

        ph_lat = "N000.00"
        ph_long = "W000.00"
        
        VBoxLayout = QVBoxLayout()
        
        top_label_title = QLabel("Left Top")
        top_label_lat = QLabel("Latitude: ")
        self.top_edit_lat = LLLineEdit(self.parent.boundary['lat1'])
        self.top_edit_lat.setValidator(valid_lat)
        self.top_edit_lat.setPlaceholderText(ph_lat)
        top_label_long = QLabel("Longitude: ")
        self.top_edit_long = LLLineEdit(self.parent.boundary['long1'])
        self.top_edit_long.setValidator(valid_long)
        self.top_edit_long.setPlaceholderText(ph_long)

        top_HBoxLayout = QHBoxLayout()
        top_HBoxLayout.addWidget(top_label_lat)
        top_HBoxLayout.addWidget(self.top_edit_lat)
        top_HBoxLayout.addWidget(top_label_long)
        top_HBoxLayout.addWidget(self.top_edit_long)
        
        bottom_label_title = QLabel("Right Bottom")
        bottom_label_lat = QLabel("Latitude: ")
        self.bottom_edit_lat = LLLineEdit(self.parent.boundary['lat2'])
        self.bottom_edit_lat.setValidator(valid_lat)
        self.bottom_edit_lat.setPlaceholderText(ph_lat)
        bottom_label_long = QLabel("Longitude: ")
        self.bottom_edit_long = LLLineEdit(self.parent.boundary['long1'])
        self.bottom_edit_long.setValidator(valid_long)
        self.bottom_edit_long.setPlaceholderText(ph_long)

        bottom_HBoxLayout = QHBoxLayout()
        bottom_HBoxLayout.addWidget(bottom_label_lat)
        bottom_HBoxLayout.addWidget(self.bottom_edit_lat)
        bottom_HBoxLayout.addWidget(bottom_label_long)
        bottom_HBoxLayout.addWidget(self.bottom_edit_long)

        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")
        save_btn.clicked.connect(self.saveSettings)
        cancel_btn.clicked.connect(self.cancelSettings)
        confirm_HBoxLayout = QHBoxLayout()
        confirm_HBoxLayout.addStretch()
        confirm_HBoxLayout.addWidget(save_btn)
        confirm_HBoxLayout.addWidget(cancel_btn)


        VBoxLayout.addWidget(top_label_title)
        VBoxLayout.addLayout(top_HBoxLayout)
        VBoxLayout.addWidget(bottom_label_title)
        VBoxLayout.addLayout(bottom_HBoxLayout)
        VBoxLayout.addLayout(confirm_HBoxLayout)

        self.setLayout(VBoxLayout)

    def saveSettings(self):
        self.accept()
        lat1 = self.top_edit_lat.text()
        long1 = self.top_edit_long.text()
        lat2 = self.bottom_edit_lat.text()
        long2 = self.bottom_edit_long.text()
        if len(lat1) == 8:
            lat1 += "00.000"
        if len(long1) == 8:
            long1 += "00.000"
        if len(lat2) == 8:
            lat2 += "00.000"
        if len(long2) == 8:
            long2 += "00.000"
        self.parent.setLatLong(
            lat1,
            long1,
            lat2,
            long2
            )
        return

    def cancelSettings(self):
        self.reject()
        return

    def exec_(self):
        lat1 = self.parent.boundary['lat1']
        long1 = self.parent.boundary['long1']
        lat2 = self.parent.boundary['lat2']
        long2 = self.parent.boundary['long2']
        self.top_edit_lat.setText(lat1)
        self.top_edit_long.setText(long1)
        self.bottom_edit_lat.setText(lat2)
        self.bottom_edit_long.setText(long2)
        super().exec_()

class LLLineEdit(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.textChanged.connect(self.onTextChanged)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Backspace:
            if len(self.text()) == 2:
                if len(self.selectedText()) == 0:
                    self.setSelection(0, 2)
                    return
            elif len(self.text()) in [5, 8, 11]:
                if len(self.selectedText()) == 0:
                    self.setSelection(len(self.text()) - 3, len(self.text()))
                    return
        super().keyPressEvent(event)

    def onTextChanged(self, text):
        self.setText(self.text().upper())
        if len(self.text()) == 1 and self.text().upper() in ["N", "S"]:
            self.setText(self.text() + "0")

        if len(self.text()) in [4, 7, 10]:
            self.setText(self.text() + ".")