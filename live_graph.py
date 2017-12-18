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
import pandas as pd
from PlotDefinition import PlotDefinition

#TODO: proper data stream (database?)
#TODO: plot parameter input ala autoplot.py
#TODO: function where I can feed plot parameters and automatically generate plots and data update functions (probably needs to be a class)
#       make_plot is a jank step in that direction (parameters are attrocious)
#       need to calculate subplot layout given n number of graphs
#       this is going to be tricky (FML)
#       or allow configuration in gui given pandas dataframe
#TODO: add numerical fields (not just graphs)

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

#number of datapoints to store/retrieve
data_range = 200

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
#TODO: switch to pandas dataframe to imitate SQL table/database
cols = ['time', 'cos(x)', '-cos(x)', 'cos(x) + -cos(x)']
database = pd.DataFrame(columns=cols)

#function to add plotItems to GraphicsLayout and format them
def make_plot(coord, data_style, title='', xlab='', ylab=''):
    plot = []
    plot.append(plot_box.addPlot(row=coord[0], col=coord[1], title=title, labels={"left":ylab,"bottom":xlab}))
    plot[0].addLegend()
    print(data_style)
    for dataset in data_style:
        plot.append(plot[0].plot(name=dataset[0], pen=dataset[1]))
    return plot

#make plots
p1 = PlotDefinition((0,0), title='cos', xlabel='time(s)')
p2 = PlotDefinition((0,1), title='-cos', xlabel='time(s)')
p3 = PlotDefinition((1,0), title='destructive interference', xlabel='time(s)')
p4 = PlotDefinition((1,1), title='cos and -cos', xlabel='time(s)')

p1.setX('time')
p2.setX('time')
p3.setX('time')
p4.setX('time')

p1.addY('cos(x)','r')
p2.addY('-cos(x)','g')
p3.addY('cos(x) + -cos(x)','b')
p4.addY('cos(x)','r')
p4.addY('-cos(x)','g')

p1.makePlot(plot_box)
p2.makePlot(plot_box)
p3.makePlot(plot_box)
p4.makePlot(plot_box)

#fake data stream in place of serial or some other type of read in
def fake_data():
    t = pg.ptime.time() - start_time
    y1 = np.cos(2 * np.pi * (t%500))
    y2 = -np.cos(2 * np.pi * (t%500))
    return [t,y1,y2]

#update function runs on each tick
def update():
    global database, cols

    #get data
    t,y1,y2 = fake_data()
    y3 = y1+y2

    #update database
    database = database.append(pd.DataFrame([[t,y1,y2,y3]],columns=cols))

    #slice off out of range data
    database = database.tail(data_range)

    #update plots with new data
    p1.updatePlot(database)
    p2.updatePlot(database)
    p3.updatePlot(database)
    p4.updatePlot(database)

#display window
#TODO: figure out window sizing (WTF WHY U NO WORK NO MATTER WHAT I TRY IT STILL CUTS OFF PARTS OF RIGHT MOST PLOTS)
w.show()

#timer and tick updates
timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(100) # 10hz

## Start the Qt event loop
app.exec_()
