import sys
import cv2
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from bs4 import BeautifulSoup as bs
import urllib.request as req
from tesy_ui import Ui_MainWindow
import time

class Example(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.timer = QTimer()
        self.timer.timeout.connect(self.chk)
        self.timer.setInterval(1 * 1000)
        self.rb_1s.setChecked(True)
        self.show()

    def setCycle(self):
        if self.rb_5m.isChecked():
            self.timer.setInterval(5*60*1000)
        elif self.rb_3m.isChecked():
            self.timer.setInterval(3*60*1000)
        elif self.rb_1m.isChecked():
            self.timer.setInterval(1*60*1000)
        elif self.rb_10s.isChecked():
            self.timer.setInterval(10*1000)
        else:
            self.timer.setInterval(1*1000)

    def startChk(self):
        self.lineEdit.setEnabled(False)
        self.timer.start()

    def stopChk(self):
        self.lineEdit.setEnabled(True)
        self.timer.stop()

    def chk(self):
        self.rsp = req.urlopen(self.lineEdit.text())
        self.html = bs(self.rsp, "html.parser")
        try:
            self.test = self.html.find(alt="UP").attrs["alt"]
        except:
            self.test = "XX"
        self.t = time.localtime()
        self.label_2.setText(f"{self.t.tm_hour}:{self.t.tm_min}:{self.t.tm_sec} 체크결과: {self.test}")
# class Example(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Cam_exam")
#         self.setGeometry(150,150,650,540)
#         self.initUI()
#     def initUI(self):
#         self.cap = cv2.VideoCapture(0)
#         self.fps = 24
#         self.frame = QLabel(self)
#         self.frame.resize(640, 480)
#         self.frame.setScaledContents(True)
#         self.frame.move(5,5)
#
#         self.timer = QTimer()
#         self.timer.timeout.connect(self.nextFrameSlot)
#         self.timer.start(1000. / self.fps)
#
#         self.show()
#
#     def keyPressEvent(self, e):
#         if e.key() == Qt.Key_Escape:
#             self.frame.setPixmap(QPixmap.fromImage(QImage()))
#             self.timer.stop()
#     def nextFrameSlot(self):
#         _, frame = self.cap.read()
#         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
#         pix = QPixmap.fromImage(img)
#         self.frame.setPixmap(pix)


app = QApplication(sys.argv)
mainWindow = Example()
sys.exit(app.exec_())
