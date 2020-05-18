import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QScrollArea
from PyQt5.QtWidgets import QDesktopWidget, QMenu, QAction
from PyQt5.QtGui import QIcon, QPixmap

from frame import QMainFrame
from load_mva import QLoadMVADialog

default_bg = "C:/Users/tzchao/Desktop/MVA.JPG"

class App(QMainWindow):
    def __init__(self, size:tuple=None):
        super().__init__()
        self.title = "Euroscope Sector File Drawer"
        if size:
            self.top = 30
            self.left = size[0] // 2
            self.width = size[0] // 2
            self.height = size[1] - 80
        else:
            self.top = 40
            self.left = 40
            self.width = 1600
            self.height = 1200

        self.loaded_mva_text = """
RCTP_MVA N025.55.00.000 E120.20.00.000 N025.55.00.000 E122.15.00.000
RCTP_MVA N025.55.00.000 E122.15.00.000 N024.10.00.000 E122.15.00.000
RCTP_MVA N024.10.00.000 E122.15.00.000 N024.10.00.000 E120.20.00.000
RCTP_MVA N024.10.00.000 E120.20.00.000 N025.55.00.000 E120.20.00.000
RCTP_MVA N025.23.50.816 E121.33.27.949 N025.10.34.370 E121.57.27.670
RCTP_MVA N025.10.34.370 E121.57.27.670 N025.00.32.826 E122.05.24.683
RCTP_MVA N025.00.32.826 E122.05.24.683 N024.54.27.968 E121.56.12.824
RCTP_MVA N024.54.27.968 E121.56.12.824 N025.00.08.896 E121.51.35.684
RCTP_MVA N025.00.08.896 E121.51.35.684 N025.01.56.122 E121.44.05.574
RCTP_MVA N025.01.56.122 E121.44.05.574 N025.01.52.860 E121.39.33.092
RCTP_MVA N025.01.52.860 E121.39.33.092 N025.04.45.985 E121.39.21.045
RCTP_MVA N025.04.45.985 E121.39.21.045 N025.04.43.871 E121.38.33.251
RCTP_MVA N025.04.43.871 E121.38.33.251 N025.02.53.231 E121.36.40.263
RCTP_MVA N025.02.53.231 E121.36.40.263 N025.06.21.100 E121.29.32.879
RCTP_MVA N025.06.21.100 E121.29.32.879 N025.13.46.631 E121.21.40.818
RCTP_MVA N025.13.46.631 E121.21.40.818 N025.23.50.816 E121.33.27.949
RCTP_MVA N025.10.53.443 E121.24.45.368 N025.21.32.460 E121.37.35.675
RCTP_MVA N025.19.07.004 E121.41.55.583 N025.05.39.395 E121.38.41.956
RCTP_MVA N025.05.39.395 E121.38.41.956 N025.05.27.261 E121.31.08.373
RCTP_MVA N025.13.46.631 E121.21.40.818 N025.11.05.853 E121.17.53.304
RCTP_MVA N025.10.53.443 E121.24.45.368 N025.08.01.929 E121.20.22.625
RCTP_MVA N025.11.05.853 E121.17.53.304 N025.08.01.929 E121.20.22.625
RCTP_MVA N025.08.01.929 E121.20.22.625 N025.04.36.686 E121.24.04.150
RCTP_MVA N025.04.36.686 E121.24.04.150 N025.04.41.729 E121.27.35.828
RCTP_MVA N025.04.41.729 E121.27.35.828 N025.06.23.426 E121.29.32.237
RCTP_MVA N025.01.52.860 E121.39.33.092 N025.01.07.525 E121.39.35.994
RCTP_MVA N025.01.07.525 E121.39.35.994 N025.00.51.182 E121.34.10.262
RCTP_MVA N025.00.51.182 E121.34.10.262 N024.59.22.138 E121.34.13.411
RCTP_MVA N024.59.22.138 E121.34.13.411 N024.59.11.089 E121.28.11.076
RCTP_MVA N024.59.11.089 E121.28.11.076 N024.54.30.641 E121.28.28.581
RCTP_MVA N024.54.30.641 E121.28.28.581 N024.55.14.176 E121.44.05.911
RCTP_MVA N024.57.15.013 E121.28.17.565 N024.57.22.487 E121.30.65.237
RCTP_MVA N024.57.22.487 E121.30.65.237 N024.55.35.460 E121.38.58.413
RCTP_MVA N024.55.35.460 E121.38.58.413 N024.58.16.878 E121.43.04.419
RCTP_MVA N024.58.16.878 E121.43.04.419 N024.59.29.915 E121.46.44.771
RCTP_MVA N024.59.29.915 E121.46.44.771 N024.54.27.968 E121.56.12.824
RCTP_MVA N024.55.35.460 E121.38.58.413 N025.00.54.797 E121.38.31.026
RCTP_MVA N024.55.14.176 E121.44.05.911 N024.47.26.735 E121.57.16.505
RCTP_MVA N024.54.27.968 E121.56.12.824 N024.47.26.735 E121.57.16.505
RCTP_MVA N024.54.27.968 E121.56.12.824 N024.54.43.111 E122.00.24.455
RCTP_MVA N024.48.45.814 E121.57.04.453 N024.48.55.381 E122.00.47.043
RCTP_MVA N024.54.43.111 E122.00.24.455 N024.48.55.381 E122.00.47.043
RCTP_MVA N025.06.20.206 E121.22.15.115 N025.03.34.098 E121.16.42.596
RCTP_MVA N025.03.34.098 E121.16.42.596 N024.54.22.596 E121.17.55.430
RCTP_MVA N024.54.22.596 E121.17.55.430 N024.56.05.647 E121.24.47.771
RCTP_MVA N024.56.05.647 E121.24.47.771 N024.55.68.000 E121.28.28.025
RCTP_MVA N025.03.34.098 E121.16.42.596 N024.56.16.208 E121.08.10.456
RCTP_MVA N024.56.16.208 E121.08.10.456 N024.57.10.113 E121.17.30.498
RCTP_MVA N024.56.16.208 E121.08.10.456 N024.49.29.460 E120.57.55.889
RCTP_MVA N024.54.22.596 E121.17.55.430 N024.48.05.433 E121.04.49.168
RCTP_MVA N024.54.50.706 E121.06.00.568 N024.48.38.431 E121.06.00.550
RCTP_MVA N024.49.29.460 E120.57.55.889 N024.41.50.000 E120.51.30.000
RCTP_MVA N024.41.50.000 E120.51.30.000 N024.41.50.000 E120.40.90.000
RCTP_MVA N024.41.50.000 E120.40.90.000 N024.30.90.000 E120.33.15.000
RCTP_MVA N024.30.90.000 E120.33.15.000 N024.11.50.000 E120.20.00.000
RCTP_MVA N024.30.90.000 E120.33.15.000 N024.30.50.000 E120.46.10.000
RCTP_MVA N024.30.50.000 E120.46.10.000 N024.37.45.000 E120.49.60.000
RCTP_MVA N024.37.45.000 E120.49.60.000 N024.40.00.000 E120.51.70.000
RCTP_MVA N024.40.00.000 E120.51.70.000 N024.41.41.000 E120.53.50.000
RCTP_MVA N024.41.41.000 E120.53.50.000 N024.53.00.000 E121.03.15.000
RCTP_MVA N024.30.50.000 E120.46.10.000 N024.27.90.000 E120.50.00.000
RCTP_MVA N024.27.90.000 E120.50.00.000 N024.10.00.000 E120.46.00.000
RCTP_MVA N024.27.90.000 E120.50.00.000 N024.34.20.000 E120.51.10.000
RCTP_MVA N024.34.20.000 E120.51.10.000 N024.34.20.000 E120.52.75.000
RCTP_MVA N024.34.20.000 E120.52.75.000 N024.39.30.000 E120.58.60.000
RCTP_MVA N024.39.30.000 E120.58.60.000 N024.39.90.000 E120.52.40.000
RCTP_MVA N024.39.30.000 E120.58.60.000 N024.41.50.000 E121.01.50.000
RCTP_MVA N024.41.50.000 E121.01.50.000 N024.43.10.000 E121.03.10.000
RCTP_MVA N024.43.10.000 E121.03.10.000 N024.48.05.433 E121.04.49.168
RCTP_MVA N024.41.50.000 E121.01.50.000 N024.41.45.000 E121.06.00.000
RCTP_MVA N024.41.45.000 E121.06.00.000 N024.48.25.000 E121.12.30.000
RCTP_MVA N024.48.25.000 E121.12.30.000 N024.54.30.641 E121.28.28.581
RCTP_MVA N024.27.90.000 E120.50.00.000 N024.30.30.000 E120.53.35.000
RCTP_MVA N024.30.30.000 E120.53.35.000 N024.34.55.000 E120.56.10.000
RCTP_MVA N024.34.55.000 E120.56.10.000 N024.35.47.403 E120.58.19.938 
RCTP_MVA N024.35.47.403 E120.58.19.938 N024.38.05.000 E121.05.05.000
RCTP_MVA N024.38.05.000 E121.05.05.000 N024.41.45.000 E121.10.35.000
RCTP_MVA N024.41.45.000 E121.10.35.000 N024.48.30.581 E121.22.16.530
RCTP_MVA N024.48.30.581 E121.22.16.530 N024.49.20.000 E121.27.05.000
RCTP_MVA N024.49.20.000 E121.27.05.000 N024.42.50.000 E121.32.00.000
RCTP_MVA N024.42.50.000 E121.32.00.000 N024.38.55.000 E121.32.00.000
RCTP_MVA N024.35.47.403 E120.58.19.938 N024.35.20.000 E121.10.20.000
RCTP_MVA N024.35.20.000 E121.10.20.000 N024.34.15.000 E121.08.55.000
RCTP_MVA N024.34.15.000 E121.08.55.000 N024.19.00.000 E120.55.50.000
RCTP_MVA N024.19.00.000 E120.55.50.000 N024.10.00.000 E120.56.05.000
RCTP_MVA N024.35.20.000 E121.10.20.000 N024.37.35.000 E121.13.05.000
RCTP_MVA N024.37.35.000 E121.13.05.000 N024.39.20.000 E121.15.20.000
RCTP_MVA N024.39.20.000 E121.15.20.000 N024.39.20.000 E121.32.00.000
RCTP_MVA N024.10.00.000 E120.58.05.000 N024.30.05.000 E121.11.55.000
RCTP_MVA N024.30.05.000 E121.11.55.000 N024.26.00.000 E121.33.35.000
RCTP_MVA N024.26.00.000 E121.33.35.000 N024.10.00.000 E121.43.35.000
RCTP_MVA N024.37.35.000 E121.13.05.000 N024.29.35.000 E121.31.00.000
RCTP_MVA N024.29.35.000 E121.31.00.000 N024.26.00.000 E121.33.35.000 
RCTP_MVA N024.54.55.000 E121.30.35.000 N024.53.25.000 E121.30.35.000
RCTP_MVA N024.53.25.000 E121.30.35.000 N024.49.00.000 E121.40.05.000
RCTP_MVA N024.49.00.000 E121.40.05.000 N024.39.00.000 E121.40.00.000
RCTP_MVA N024.38.55.000 E121.40.00.000 N024.38.55.000 E121.32.00.000
RCTP_MVA N024.39.00.000 E121.40.00.000 N024.11.35.000 E121.47.55.000
RCTP_MVA N024.11.35.000 E121.47.55.000 N024.10.00.000 E121.47.00.000
RCTP_MVA N024.39.00.000 E121.40.00.000 N024.39.00.000 E121.58.00.000
RCTP_MVA N024.39.00.000 E121.58.00.000 N024.35.55.000 E121.58.20.000
RCTP_MVA N024.35.55.000 E121.58.20.000 N024.27.30.000 E121.56.35.000
RCTP_MVA N024.27.30.000 E121.56.35.000 N024.16.25.000 E121.51.00.000
RCTP_MVA N024.16.25.000 E121.51.00.000 N024.11.35.000 E121.47.55.000
RCTP_MVA N024.39.00.000 E121.58.00.000 N024.47.26.735 E121.57.16.505
"""

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.status_bar = self.statusBar()

        self.setAcceptDrops(True)
        self.main_frame = QMainFrame(self)
        self.setCentralWidget(self.main_frame.widget)

        if default_bg:
            self.main_frame.setBackgroundPath(default_bg)
            self.main_frame.background.setLoadedMVAText(self.loaded_mva_text)


        self.setupMenuBar()
        # self.status_bar.showMessage("test status bar")
        self.show()

    def keyPressEvent(self, event):
        if QApplication.keyboardModifiers() == Qt.ControlModifier:
            self.setCursor(Qt.CrossCursor)
            self.update()
        if event.key() == Qt.Key_Escape:
            exit(1)

    def setupMenuBar(self):
        menu_bar = self.menuBar()

        self.setupDialogs()
        
        load = QMenu("Load", self)
        load_mva = QAction("Load MVA", self)
        load_mva.triggered.connect(self.loadMVADialog.exec_)
        load.addAction(load_mva)
        
        llsetings = QMenu("Lat/Long Settings", self)
        set_cropll = QAction("Crop Lat/Long Range", self)
        set_setll = QAction("Set Lat/Long Range", self)
        self.show_ll = QAction("Show Lat/Long Range", self, checkable=True)
        edit_ll = QAction("Edit Lat/Long Range", self, checkable=True)
        # show_ll.setChecked(True)
        # self.main_frame.background.showBoundary(True)
        set_cropll.triggered.connect(self.main_frame.background.setBoundary)
        set_setll.triggered.connect(self.main_frame.background.set_lat_long.exec_)
        self.show_ll.triggered.connect(self.main_frame.background.showBoundary)
        # edit_ll.triggered.connect(self.main_frame.background.editBoundary)
        llsetings.addAction(set_cropll)
        llsetings.addAction(set_setll)
        llsetings.addAction(self.show_ll)
        # llsetings.addAction(edit_ll)
        
        views = QMenu("View", self)
        set_tmask = QAction("Set Transparent Mask", self, checkable=True)
        show_loaded_mva = QAction("Show Loaded MVA", self, checkable=True)
        show_loaded_mva.setChecked(True)
        self.main_frame.background.setShowLoadedMVA(True)
        set_tmask.triggered.connect(self.main_frame.background.setTransMask)
        show_loaded_mva.triggered.connect(self.main_frame.background.setShowLoadedMVA)
        views.addAction(set_tmask)
        views.addAction(show_loaded_mva)

        menu_bar.addMenu(load)
        menu_bar.addMenu(llsetings)
        menu_bar.addMenu(views)
        return menu_bar

    def setupDialogs(self):
        self.loadMVADialog = QLoadMVADialog(self)

    def setLoadedMVAText(self, txt):
        self.loaded_mva_text = txt
        self.main_frame.background.setLoadedMVAText(txt)

    def dragEnterEvent(self, event):
        m = event.mimeData()
        if m.hasUrls():
            event.accept()
        else:
            print("ignore")
            event.ignore()

    def dropEvent(self, event):
        m = event.mimeData()
        if m.hasUrls():
            print(m.urls()[0].toLocalFile())
            self.main_frame.setBackgroundPath(m.urls()[0].toLocalFile())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    ex = App(size=(screen.size().width(), screen.size().height()))
    sys.exit(app.exec_())