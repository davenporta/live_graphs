class PlotDefinition:

    def __init__(self, coords, title='', xlabel='', ylabel=''):
        self.data = []
        self.range = 100
        self.plots = []
        self.been_ploted = False

        self.coords = coords
        self.title = title
        self.labels = {"left":ylabel,"bottom":xlabel}

    def setX(self, xHeader):
        self.x = xHeader

    def addY(self, yHeader, style):
        self.data.append([yHeader, style])

    def make_plot(self, plot_box):
        if not self.been_ploted:
            self.parent = plot_box.addPlot(row=self.coords[0], col=self.coords[1], title=self.title, labels=self.labels)
            self.parent.addLegend()
            for dataset in self.data:
                self.plots.append(self.parent.plot(name=dataset[0], pen=dataset[1]))
            self.been_ploted = True
