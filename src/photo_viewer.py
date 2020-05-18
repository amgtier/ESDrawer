from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsRectItem, QFrame
from PyQt5.QtCore import Qt, QRectF, QLineF, QPoint
from PyQt5.QtGui import QBrush, QColor, QPixmap, QPen, QPainter, QCursor

import utils
from set_lat_long import QSetLatLong

LINE_COLOR = QColor(200, 0, 0, 200)
LINE_WIDTH = 5
FOCUS_COLOR = Qt.black
FOCUS_PENSTYLE = Qt.DashLine
FOCUS_EDGE = 25
FOCUS_WIDTH = 3
DRAG_EDIT_RANGE = 10

class QPhotoViewer(QGraphicsView): 
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self._zoom = 0
        self._empty = True
        self._scene = QGraphicsScene(self)
        self._photo = QGraphicsPixmapItem()

        self.drag_to_move = None
        self.drag_to_draw = None
        self.hover_on_focus = False
        self.drag_to_edit = None
        self.boundary = {
            'status': 'set', ### 'unset', 'setting', 'set', 'dragging', 'editing'
            'coor': None, 
            'rect': None, 
            'show': False,
            'lat1': None,
            'long1': None,
            'lat2': None,
            'long2': None,
        }
        self.edit_boundary = None

        self._scene.addItem(self._photo)
        self.setScene(self._scene)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)

        self.setBackgroundBrush(QBrush(QColor(30, 30, 30)))
        self.setFrameShape(QFrame.NoFrame)

        self.draw_shape = "line"
        self.trans_mask = None
        self.trans_mask_set = False
        self.lines = []
        self.show_loaded_mva = False
        self.loaded_mva = []
        self.focus_rect = []

        self.set_lat_long = QSetLatLong(self)

        ### default boundary
        self.boundary['coor'] = (117.22423122890177, 2447.897109755766, 2199.73954394698, 1003.140339955673)
        self.boundary['lat1'] = "N025.30.00.000"
        self.boundary['long1'] = "W120.20.00.000"
        self.boundary['lat2'] = "N024.20.00.000"
        self.boundary['long2'] = "W122.10.00.000"
        self.endSetBoundary(editLL=False)

    def setPhotoPath(self, path: str):
        self.setPhoto(QPixmap(path))

    def hasPhoto(self):
        return not self._photo.pixmap().isNull()

    def fitInView(self, scale=True):
        rect = QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.hasPhoto():
                unity = self.transform().mapRect(QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                    viewrect.height() / scenerect.height())
                self.scale(factor, factor)
            self._zoom = 0

    def setPhoto(self, pixmap: QPixmap):
        self._zoom = 0
        if pixmap and not pixmap.isNull():
            self.empty = False
            self._photo.setPixmap(pixmap)
            self.fitInView()

    def wheelEvent(self, event):
        if self.hasPhoto():
            if self._zoom == 0:
                self.fitInView()
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom == 0:
                self.fitInView()
            else:
                self._zoom = 0

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.clearFocusPts()
            self.setCursor(Qt.CrossCursor)
            self.draw_shape = "rect"
        self.parent.MainWindow.keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.setCursor(Qt.ArrowCursor)
            self.draw_shape = "line"
        self.parent.MainWindow.keyPressEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.drag_to_move = event.pos()
            self.setCursor(Qt.ClosedHandCursor)
        elif event.button() == Qt.LeftButton:
            if self.boundary['status'] == 'editing':
                self.editBoundaryMousePress(event)
            elif self.hover_on_focus:
                self.drag_to_edit = self.mapToScene(event.pos())
            else:
                self.drag_to_draw = self.mapToScene(event.pos())
                self.clearFocusPts()
            if self.boundary['status'] == "setting":
                self.boundary['status'] = "dragging"
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self.drag_to_move:
            self.drag_to_move = None
        elif self.drag_to_draw:
            x1 = self.drag_to_draw.x()
            x2 = self.mapToScene(event.pos()).x()
            y1 = self.drag_to_draw.y()
            y2 = self.mapToScene(event.pos()).y()
            if self.boundary['status'] == 'dragging':
                self.boundary['coor'] = (x1, y1, x2, y2)
                self.endSetBoundary()
            elif self.draw_shape == "line":
                self.newMVA(x1, y1, x2, y2)
            self.drag_to_draw = None
        elif self.drag_to_edit:
            self.clearSceneDraw()
            if self.boundary['status'] == 'editing':
                self.editBoundaryMouseRelease(event)
            else:
                self.dragLineEndMouseRelease(event)
        if self.boundary["status"] == "setting":
            self.setCursor(Qt.CrossCursor)
        else:
            self.setCursor(Qt.ArrowCursor)
        self.hover_on_focus = None
        self.clearSceneDraw()
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if self.drag_to_move:
            self.translate(self.drag_to_move.x(), self.drag_to_move.y())
        elif self.drag_to_draw:
            x1 = self.drag_to_draw.x()
            x2 = self.mapToScene(event.pos()).x()
            y1 = self.drag_to_draw.y()
            y2 = self.mapToScene(event.pos()).y()

            self.clearSceneDraw()

            if self.draw_shape == "line":
                self._scene.addLine(QLineF(x1, y1, x2, y2), pen=QPen(LINE_COLOR, LINE_WIDTH))
            elif self.draw_shape == "rect":
                self._scene.addRect(x1, y1, x2 - x1, y2 - y1, pen=QPen(LINE_COLOR, LINE_WIDTH))
                self.selectLines(x1, y1, x2, y2)
        elif self.drag_to_edit:
            self.clearSceneDraw()
            delta_x = self.mapToScene(event.pos()).x() - self.drag_to_edit.x()
            delta_y = self.mapToScene(event.pos()).y() - self.drag_to_edit.y()
            for rect in self.focus_rect:
                idx = rect['idx']
                x1 = self.lines[idx][0]
                y1 = self.lines[idx][1]
                x2 = self.lines[idx][2]
                y2 = self.lines[idx][3]
                if rect['hover'] and rect['seq'] == 0:
                    x1 += delta_x
                    y1 += delta_y
                else:
                    x2 += delta_x
                    y2 += delta_y
                self._scene.addLine(QLineF(x1, y1, x2, y2), pen=QPen(LINE_COLOR, LINE_WIDTH))
        else:
            if self.boundary['status'] == 'editing':
                self.editBoundaryMouseMove(event)
            else:
                self.dragLineEndMouseMove(event)

        mouse_latlong = self.coorToLatLong(self.mapToScene(event.pos()).x(), self.mapToScene(event.pos()).y())
        self.parent.MainWindow.status_bar.showMessage(f"{mouse_latlong[0]}, {mouse_latlong[1]}")
        super().mouseMoveEvent(event)

    def drawForeground(self, painter, rect):
        pen = QPen(LINE_COLOR)
        pen.setWidth(5)
        painter.setPen(pen)

        _l = []
        for pt in self.lines:
            _l.append(QLineF(*pt))
        painter.drawLines(_l)

        if self.show_loaded_mva:
            pen = QPen(Qt.red, LINE_WIDTH, Qt.DashLine)
            painter.setPen(pen)
            _l = []
            for pt in self.loaded_mva:
                coor = pt['coor']
                _l.append(QLineF(*coor))
            painter.drawLines(_l)

        dotted_pen = QPen(FOCUS_COLOR, FOCUS_WIDTH, FOCUS_PENSTYLE)
        painter.setPen(dotted_pen)
        _r = []
        for rect in self.focus_rect:
            _r.append(QRectF(rect['x1'], rect['y1'], FOCUS_EDGE, FOCUS_EDGE))
        painter.drawRects(_r)

    def setTransMask(self, val):
        if val:
            if self.trans_mask is None:
                self.trans_mask = QGraphicsRectItem(0, 0, self._photo.pixmap().width(), self._photo.pixmap().height())
                self._scene.addItem(self.trans_mask)
            self.trans_mask.setBrush(QBrush(QColor(210, 210, 210, 127)))
            self.trans_mask_set = True
        else:
            if self.trans_mask is not None:
                self.trans_mask.setBrush(QBrush(QColor(210, 210, 210, 0)))
            self.trans_mask_set = False

    def dragLineEndMouseMove(self, event):
        x = self.mapToScene(event.pos()).x()
        y = self.mapToScene(event.pos()).y()
        for rect in self.focus_rect:
            if utils.ptInRange(x, y, rect['x1'], rect['y1'], rect['x2'], rect['y2']):
                rect['hover'] = True
                self.setCursor(Qt.OpenHandCursor)
                self.hover_on_focus = True
            else:
                rect['hover'] = False
        else:
            if self.cursor().shape() == Qt.OpenHandCursor:
                self.setCursor(Qt.ArrowCursor)

    def selectLines(self, x1, y1, x2, y2):
        self.clearFocusPts()
        if len(self.focus_rect) > 0: return
        for idx, pt in enumerate(self.lines):
            if utils.ptInRange(pt[0], pt[1], x1, y1, x2, y2):
                self.focus_rect = [{
                    'idx': idx,
                    'seq': 0,
                    'x1': pt[0] - FOCUS_EDGE // 2,
                    'y1': pt[1] - FOCUS_EDGE // 2,
                    'x2': pt[0] + FOCUS_EDGE // 2,
                    'y2': pt[1] + FOCUS_EDGE // 2,
                    'hover': False,
                }]
            if utils.ptInRange(pt[2], pt[3], x1, y1, x2, y2):
                self.focus_rect = [{
                    'idx': idx,
                    'seq': 1,
                    'x1': pt[2] - FOCUS_EDGE // 2,
                    'y1': pt[3] - FOCUS_EDGE // 2,
                    'x2': pt[2] + FOCUS_EDGE // 2,
                    'y2': pt[3] + FOCUS_EDGE // 2,
                    'hover': False,
                }]

    def clearSceneDraw(self):
        for i in self._scene.items(order=Qt.DescendingOrder):
            if i != self._photo:
                i.setParentItem(None)

    def clearFocusPts(self):
        self.focus_rect = []

    def setBoundary(self):
        self.setTransMask(True)
        self.setCursor(Qt.CrossCursor)
        self.boundary['status'] = 'setting'
        self.draw_shape = "rect"

    def editBoundary(self, val):
        if val:
            self.boundary['status'] = 'editing'
        else:
            if self.boundary['rect'] is None:
                self.boundary['status'] = 'unset'
            else:
                self.boundary['status'] = 'set'

    def editBoundaryMousePress(self, event):
        self.edit_boundary = {'pt': self.editBoundaryPt(event), 'coor': self.mapToScene(event.pos())}

    def editBoundaryMouseMove(self, event):
        if self.edit_boundary is None:
            pt = self.editBoundaryPt(event)
            if pt in ['x1', 'x2']:
                cursor = Qt.SplitHCursor
            elif pt in ['y1', 'y2']:
                cursor = Qt.SplitHCursor
            else:
                cursor = Qt.ArrowCursor
            self.setCursor(cursor)
        else:
            delta_x = self.mapToScene(event.pos()).x() - self.edit_boundary['coor'].x()
            delta_y = self.mapToScene(event.pos()).y() - self.edit_boundary['coor'].y()
            x1 = self.boundary['coor'][0]
            y1 = self.boundary['coor'][1]
            x2 = self.boundary['coor'][2]
            y2 = self.boundary['coor'][3]
            if self.edit_boundary['pt'] == 'x1':
                x1 += delta_x
            elif self.edit_boundary['pt'] == 'x2':
                y1 = self.boundary['coor'][1]
                x2 += delta_x
            elif self.edit_boundary['pt'] == 'y1':
                y1 += delta_y
            elif self.edit_boundary['pt'] == 'y2':
                y2 += delta_y
            self.boundary['coor'] = (x1, y1, x2, y2)
            self.drawBoundary(False)


    def editBoundaryPt(self, event):
        x = self.mapToScene(event.pos()).x()
        y = self.mapToScene(event.pos()).y()
        bound_x1 = self.boundary['coor'][0]
        bound_y1 = self.boundary['coor'][1]
        bound_x2 = self.boundary['coor'][2]
        bound_y2 = self.boundary['coor'][3]
        if bound_x1 > bound_x2:
            bound_x1, bound_x2 = bound_x2, bound_x1
        if bound_y1 > bound_y2:
            bound_y1, bound_y2 = bound_y2, bound_y1
        if self.boundary['coor'][0] - DRAG_EDIT_RANGE < x < self.boundary['coor'][0] + DRAG_EDIT_RANGE and\
            bound_y1 <= y <= bound_y2:
            return 'x1'
        elif self.boundary['coor'][2] - DRAG_EDIT_RANGE < x < self.boundary['coor'][2] + DRAG_EDIT_RANGE and\
            bound_y1 <= y <= bound_y2:
            return 'x2'
        elif self.boundary['coor'][1] - DRAG_EDIT_RANGE < y < self.boundary['coor'][1] + DRAG_EDIT_RANGE and\
            bound_x1 <= x <= bound_x2:
            return 'y1'
        elif self.boundary['coor'][3] - DRAG_EDIT_RANGE < y < self.boundary['coor'][3] + DRAG_EDIT_RANGE and\
            bound_x1 <= x <= bound_x2:
            return 'y2'

    def dragLineEndMouseRelease(self, event):
        delta_x = self.mapToScene(event.pos()).x() - self.drag_to_edit.x()
        delta_y = self.mapToScene(event.pos()).y() - self.drag_to_edit.y()
        for rect in self.focus_rect:
            idx = rect['idx']
            x1 = self.lines[idx][0]
            y1 = self.lines[idx][1]
            x2 = self.lines[idx][2]
            y2 = self.lines[idx][3]
            if rect['hover'] and rect['seq'] == 0:
                x1 += delta_x
                y1 += delta_y
            else:
                x2 += delta_x
                y2 += delta_y
            self.lines[idx] = (x1, y1, x2, y2)
            rect['x1'] += delta_x
            rect['y1'] += delta_y
            rect['x2'] += delta_x
            rect['y2'] += delta_y

        self.focus_rect = []

        lines = self.lines
        self.parent.new_mva_lines.setPlainText("")
        for x1, y1, x2, y2 in lines:
            pt1 = self.coorToLatLong(x1, y1)
            pt2 = self.coorToLatLong(x2, y2)
            new_line = f"{self.parent.edit_prefix.text()} {pt1[0]} {pt1[1]} {pt2[0]} {pt2[1]}"
            self.parent.new_mva_lines.appendPlainText(new_line)

        self.drag_to_edit = None

    def endSetBoundary(self, editLL=True):
        self.setTransMask(False)
        self.setCursor(Qt.ArrowCursor)
        self.boundary['status'] = 'set'
        self.draw_shape = "line"

        if self.boundary['status'] == 'set':
            self.drawBoundary(editLL)

    def drawBoundary(self, editLL):
        x = self.boundary['coor'][0]
        y = self.boundary['coor'][1]
        w = self.boundary['coor'][2] - x
        h = self.boundary['coor'][3] - y
        self.boundary['rect'] = QGraphicsRectItem(x, y, w, h)
        self._scene.addItem(self.boundary['rect'])
        pen = QPen(QBrush(QColor(255, 210, 210, 0)), LINE_WIDTH, Qt.DashDotDotLine)
        self.boundary['rect'].setPen(pen)
        if editLL:
            result = self.set_lat_long.exec_()
            self.parent.MainWindow.show_ll.setChecked(True)
            self.showBoundary(True)
            
    def showBoundary(self, val):
        if self.boundary['status'] != 'unset':
            self.boundary['show'] = val
            if val and self.boundary is not None:
                self.boundary['rect'].setBrush(QBrush(QColor(255, 210, 210, 127)))
            else:
                self.boundary['rect'].setBrush(QBrush(QColor(255, 210, 210, 0)))
        self.update()

    def setLatLong(self, lat1, long1, lat2, long2):
        self.boundary['lat1'] = lat1
        self.boundary['long1'] = long1
        self.boundary['lat2'] = lat2
        self.boundary['long2'] = long2

    def setLoadedMVAText(self, mva):
        if len(mva) > 0:
            self.setLoadedMVA([tuple(line.split()[1:]) for line in mva.strip("\n").split("\n")])
        
    def setLoadedMVA(self, mva):
        self.loaded_mva = []
        for line in mva:
            self.loaded_mva.append({
                'll': line,
                'coor': (*self.latLongToCoor(line[0], line[1]), *self.latLongToCoor(line[2], line[3])),
                })

    def setShowLoadedMVA(self, val):
        self.show_loaded_mva = val
        self.update()

    def latLongToCoor(self, lat, longi):
        return self.longToCoor(longi), self.latToCoor(lat)

    def coorToLatLong(self, x, y):
        return self.coorToLat(y), self.coorToLong(x)

    def latToCoor(self, lat):
        bl1 = self.boundary['lat1']
        bl2 = self.boundary['lat2']
        by1 = self.boundary['coor'][1]
        by2 = self.boundary['coor'][3]
        if by1 > by2:
            by1, by2 = by2, by1
        return utils.latToCoor(lat, bl1, bl2, by1, by2)

    def longToCoor(self, longi):
        bl1 = self.boundary['long1']
        bl2 = self.boundary['long2']
        bx1 = self.boundary['coor'][0]
        bx2 = self.boundary['coor'][2]
        if bx1 > bx2:
            bx1, bx2 = bx2, bx1
        return utils.longToCoor(longi, bl1, bl2, bx1, bx2)

    def coorToLong(self, x):
        bl1 = self.boundary['long1']
        bl2 = self.boundary['long2']
        bx1 = self.boundary['coor'][0]
        bx2 = self.boundary['coor'][2]
        if bx1 > bx2:
            bx1, bx2 = bx2, bx1
        return utils.coorToLong(x, bl1, bl2, bx1, bx2, "E")

    def coorToLat(self, y):
        bl1 = self.boundary['lat1']
        bl2 = self.boundary['lat2']
        by1 = self.boundary['coor'][1]
        by2 = self.boundary['coor'][3]
        if by1 > by2:
            by1, by2 = by2, by1
        return utils.coorToLat(y, bl1, bl2, by1, by2, "N")

    def newMVA(self, x1, y1, x2, y2):
        # self.lines.append((x1, y1, x2, y2))
        pt1 = self.coorToLatLong(x1, y1)
        pt2 = self.coorToLatLong(x2, y2)
        new_line = f"{self.parent.edit_prefix.text()} {pt1[0]} {pt1[1]} {pt2[0]} {pt2[1]}"
        self.parent.new_mva_lines.appendPlainText(new_line)

    def newMvaChanged(self):
        self.newMVATxt(self.parent.new_mva_lines.toPlainText())

    def newMVATxt(self, txt):
        self.lines = []
        if txt:
            mva = [tuple(line.split()[1:]) for line in txt.strip("\n").split("\n")]
            for line in mva:
                self.lines.append((*self.latLongToCoor(line[0], line[1]), *self.latLongToCoor(line[2], line[3])))