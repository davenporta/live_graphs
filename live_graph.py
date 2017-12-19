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

settings = pd.read_csv("graph_settings.csv")

#initialize data arrays (for testing only)
#TODO: switch to pandas dataframe to imitate SQL table/database
cols = ['time', 'cos', 'neg_cos', 'destruc']
database = pd.DataFrame(columns=cols)

#list for easy iteration through plots
plots = []

#for each plot in parameters
for i in range(len(settings.index)):
    #get parameters for plot
    row = settings.ix[i]

    #plot location on screen
    subplot = (row['row'], row['col'])

    #initialize plot and add to list
    plots.append(PlotDefinition(subplot, title=row['title'], xlabel=row['xlabel']))

    #set x data
    plots[i].setX(row['x'])

    #parse y data
    ys = row['y'].split(' | ')
    pens = row['pen'].split(' | ')
    aliases = row['alias'].split(' | ')
    params = zip(ys, pens, aliases)

    #push y data to plot
    for param in params:
        plots[i].addY(param)

    #make plot and push to window
    plots[i].makePlot(plot_box)

#fake data stream in place of serial or some other type of read in
def fake_data():
    t = pg.ptime.time() - start_time
    y1 = np.cos(2 * np.pi * (t%500))
    y2 = -y1
    y3 = y1+y2
    return [t,y1,y2,y3]

#update function runs on each tick
def update():
    global database, cols

    #get data
    t,y1,y2,y3 = fake_data()

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
