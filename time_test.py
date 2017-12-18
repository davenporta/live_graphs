from PyQt5 import QtGui
from PyQt5.QtCore import Qt
import pyqtgraph as pg

app = QtGui.QApplication([])
start_time = pg.ptime.time()

def fake_data():
    t = pg.ptime.time() - start_time
    print(t)

timer = pg.QtCore.QTimer()
timer.timeout.connect(fake_data)
timer.start(500) # 0.2hz

app.exec_()
