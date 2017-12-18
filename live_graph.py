import pandas as pd
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
import pyqtgraph as pg
#import serial
import time
#from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
#import matplotlib.pyplot as plt
import numpy as np

#TODO: proper data stream
#TODO: plot parameter input ala autoplot.py
#TODO: function where I can feed plot parameters and automatically generate plots and data update functions (probably needs to be a class)
#       make_plot is a jank step in that direction (parameters are attrocious)
#       need to calculate subplot layout given n number of graphs
#       this is going to be tricky (FML)

#window title
run_name = "live graph display test"

#initialize Qt
app = QtGui.QApplication([])
#timer
start_time = pg.ptime.time()
#top level
w = QtGui.QWidget()
w.setWindowTitle(run_name)
# layout grid
layout = QtGui.QGridLayout()
w.setLayout(layout)

# Zero Indexes for the gui layout (row, column) (sternie's idea)
zr = 0
zc = 0

#number of datapoints to graph
data_range = 100

#add area for tiled plots
plot_box = pg.GraphicsLayoutWidget()
layout.addWidget(plot_box, zr+0, zc+0)

#quit application function
def exit():
    app.quit()

#quit application function
quit = QtGui.QPushButton("Quit")
quit.clicked.connect(exit)
layout.addWidget(quit, zr+1, zc+0)

#initialize data arrays (for testing only)
#TODO: switch to numpy arrays
t_arr = []
y1_arr = []
y2_arr = []
y3_arr = []

#function to add plotItems to GraphicsLayout and format them
def make_plot(coord, title, data_style):
    plot = []
    plot.append(plot_box.addPlot(row=coord[0], col=coord[1], title=title))
    plot[0].addLegend()
    for dataset in data_style:
        plot.append(plot[0].plot(name=dataset[0], pen=dataset[1]))
    return plot

#make plots
plot1 = make_plot((0,0), 'cos', [['cos(x)','r']])
plot2 = make_plot((0,1), '-cos', [['-cos(x)','g']])
plot3 = make_plot((1,0), 'destructive interference', [['cos(x) + -cos(x)','b']])
plot4 = make_plot((1,1), 'cos and -cos', [['cos(x)','r'],['-cos(x)','g']])

#fake data stream in place of serial or some other type of read in
def fake_data():
    t = pg.ptime.time() - start_time
    y1 = np.cos(2 * np.pi * (t%500))
    y2 = -np.cos(2 * np.pi * (t%500))
    return [t,y1,y2]

#update function runs on each tick
def update():
    global t_arr,y1_arr,y2_arr,y3_arr

    #get data
    t,y1,y2 = fake_data()

    #add to appropriate arrays
    t_arr.append(t)
    y1_arr.append(y1)
    y2_arr.append(y2)
    y3_arr.append(y1+y2)

    #slice off out of range data
    if (len(t_arr)>data_range):
        t_arr = t_arr[-data_range:]
        y1_arr = y1_arr[-data_range:]
        y2_arr = y2_arr[-data_range:]
        y3_arr = y3_arr[-data_range:]

    #update plots with new data
    plot1[1].setData(t_arr,y1_arr)
    plot2[1].setData(t_arr,y2_arr)
    plot3[1].setData(t_arr,y3_arr)
    plot4[1].setData(t_arr,y1_arr)
    plot4[2].setData(t_arr,y2_arr)

#display window
#TODO: figure out window sizing (WTF WHY U NO WORK NO MATTER WHAT I TRY IT STILL CUTS OFF PARTS OF RIGHT MOST PLOTS)
w.show()

#timer and tick updates
timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(100) # 10hz

## Start the Qt event loop
app.exec_()