import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QScrollArea, QFileDialog
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

        self.loaded_mva_text = ""

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
        self.show()

    def keyPressEvent(self, event):
        if QApplication.keyboardModifiers() == Qt.ControlModifier:
            self.setCursor(Qt.CrossCursor)
            self.update()
        # if event.key() == Qt.Key_Escape:
        #     exit(1)

    def setupMenuBar(self):
        menu_bar = self.menuBar()

        self.setupDialogs()
        
        load = QMenu("Load", self)
        load_mva = QAction("Load MVA", self)
        load_bg = QAction("Load Background", self)
        load_mva.triggered.connect(self.loadMVADialog.exec_)
        load_bg.triggered.connect(self.loadBackgroundFile)
        load.addAction(load_mva)
        load.addAction(load_bg)
        
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

    def loadBackgroundFile(self):
        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(self, 
            "Select Background Image", 
            "", 
            "All files(*);;", 
            options=options
            )
        if file:
            self.main_frame.setBackgroundPath(file)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    ex = App(size=(screen.size().width(), screen.size().height()))
    sys.exit(app.exec_())