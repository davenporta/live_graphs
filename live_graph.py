import pandas as pd
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
import pyqtgraph as pg
import time
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
run_name = "MASA Live Data Dashboard"

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

#max number of datapoints to store/retrieve
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

#make PlotDefinitions and add to list for easy iteration
plots = []
plots.append(PlotDefinition((0,0), title='cos', xlabel='time(s)'))
plots.append(PlotDefinition((0,1), title='-cos', xlabel='time(s)'))
plots.append(PlotDefinition((1,0), title='destructive interference', xlabel='time(s)'))
plots.append(PlotDefinition((1,1), title='cos and -cos', xlabel='time(s)'))

#set x axis (will be database["time"])
for p in plots:
    p.setX('time')

#add y datasets to each plot (note p4 has 2 datasets)
plots[0].addY('cos(x)','r')
plots[1].addY('-cos(x)','g')
plots[2].addY('cos(x) + -cos(x)','b')
plots[3].addY('cos(x)','r')
plots[3].addY('-cos(x)','g')

#make the plots and push them to window
for p in plots:
    p.makePlot(plot_box)

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
    for p in plots:
        p.updatePlot(database)

#display window
#TODO: figure out window sizing (WTF WHY U NO WORK NO MATTER WHAT I TRY THE COLUMNS ARE DIFFERENT SIZES)
w.showMaximized()

#timer and tick updates
timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(100) # 10hz

## Start the Qt event loop
app.exec_()
