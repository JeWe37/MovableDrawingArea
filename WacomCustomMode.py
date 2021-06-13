#!/usr/bin/python
import sys
import os

# Change path so we find Xlib
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Xlib.display import Display
from Xlib.ext import xinput
from Xlib.protocol import rq

import numpy as np
import subprocess

from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication

import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)

RawMotionEventData = rq.Struct(
    rq.Card16('deviceid'),
    rq.Pad(28),
    rq.List('values', xinput.FP3232('value')),
)

def setMatrix(ident, M):
    subprocess.run(['xinput', 'set-prop', str(ident), 'Coordinate Transformation Matrix', *list(map(str, M.flatten()))])

def getArea(ident):
    return np.array(list(map(int, subprocess.run(['xinput', 'list-props', str(ident)], capture_output=True).stdout.decode("utf-8").split("\n")[8].split("\t")[2].split(", ")[2:])))

class XIThread(QtCore.QThread):
    position = QtCore.pyqtSignal(int, int)
    size = QtCore.pyqtSignal(int, int)

    def coordPos(self, pos):
        return (self.A.dot(np.append(pos/self.area, 1)))[0:2]

    def scaleMat(self, x, y):
        self.A[0,0], self.A[1,1] = x, y

    def moveMat(self, pos):
        self.A[0,2], self.A[1,2] = pos

    def __init__(self, desktop, scale):
        QtCore.QThread.__init__(self)
        self.screen_dims = desktop.width(), desktop.height()
        self.correctId = None
        self.scale = scale

    def __del__(self):
        self.wait()

    def init(self, ident):
        self.correctId = ident
        self.area = getArea(self.correctId)
        self.A = np.eye(3)
        yscale_abs = int(self.screen_dims[1]*self.scale)
        xscale_abs = int(yscale_abs*self.area[0]/self.area[1])
        self.scaleMat(xscale_abs/self.screen_dims[0], self.scale)
        self.size.emit(xscale_abs, yscale_abs)
        setMatrix(self.correctId, self.A)

    def run(self):
        display = Display()
        currentPos = np.zeros(2)
        startPos = np.zeros(2)
        oldStart = np.zeros(2)
        self.position.emit(*startPos.astype(int))
        pressed = False
        try:
            extension_info = display.query_extension('XInputExtension')
            xinput_major = extension_info.major_opcode
            display.ge_add_event_data(xinput_major, xinput.RawMotion, RawMotionEventData)

            screen = display.screen()
            screen.root.xinput_select_events([
                (xinput.AllDevices, xinput.RawMotionMask | xinput.KeyPressMask | xinput.KeyReleaseMask), 
            ])
            while True:
                event = display.next_event()
                if event.evtype == xinput.RawMotion:
                    ident = event.data.deviceid
                    if self.correctId is None:
                        if "stylus" in display.xinput_query_device(ident).devices[0].name:
                            self.init(ident)
                        else:
                            continue
                    if (
                        self.correctId == ident
                        and event.type == display.extension_event.GenericEvent
                        and event.extension == xinput_major
                    ):
                        currentPos = self.coordPos(np.array(event.data.values[6:8]))
                        if pressed:
                            self.position.emit(*((oldStart+startPos-currentPos)*self.screen_dims).astype(int))
                elif event.data.detail == 65:
                    if event.evtype == xinput.KeyPress:
                        if not pressed:
                            tempMat = np.zeros((3,3))
                            tempMat[:,2] = np.append(currentPos, 1)
                            setMatrix(self.correctId, tempMat)
                            startPos = np.copy(currentPos)
                            pressed = True
                    elif event.evtype == xinput.KeyRelease:
                        oldStart = oldStart+startPos-currentPos
                        self.moveMat(oldStart)
                        setMatrix(self.correctId, self.A)
                        pressed = False
        finally:
            display.close()

class MainWindow(QMainWindow):
    def __init__(self, desktop, scale):
        QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.X11BypassWindowManagerHint
        )
        self.setStyleSheet("background-color: rgba(140,140,140, 30); ")
        self.setWindowOpacity(0.1)
        self.xi_thread = XIThread(desktop, scale)
        self.xi_thread.size.connect(self.changeSize)
        self.xi_thread.position.connect(self.changePosition)
        self.xi_thread.start()

    def changeSize(self, x, y):
        current = self.geometry()
        current.setWidth(x)
        current.setHeight(y)
        self.setGeometry(current)

    def changePosition(self, x, y):
        current = self.geometry()
        current.moveLeft(x)
        current.moveTop(y)
        self.setGeometry(current)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = MainWindow(app.desktop(), float(app.arguments()[1]))
    mywindow.show()
    app.exec_()
