from .graph import Graph
from .ann import Annotations
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np


class Spatio(Graph):
    """
        Inherits from Graph abstract base class. Creates a line plot using
        pyplot. 
    """

    def __init__(self, hrm):
        self.hrm = hrm
        self.image = None
        self.annotations = Annotations(hrm)
        self._cmap = ((0.0, 0.0, 0.5625), (0.0, 0.0, 0.6171875),
                      (0.0, 0.0, 0.671875), (0.0, 0.0, 0.7265625),
                      (0.0, 0.0, 0.78125), (0.0, 0.0, 0.8359375),
                      (0.0, 0.0, 0.890625), (0.0, 0.0, 0.9453125),
                      (0.0, 0.0, 1), (0.0, 0.25, 1),
                      (0.0, 0.5, 1), (0.0, 0.75, 1), (0.0, 1.0, 1),
                      (0.0681818202137947, 1.0, 0.931818187236786),
                      (0.136363640427589, 1.0, 0.863636374473572),
                      (0.204545468091965, 1.0, 0.795454561710358),
                      (0.272727280855179, 1.0, 0.727272748947144),
                      (0.340909093618393, 1.0, 0.659090936183929),
                      (0.409090936183929, 1.0, 0.590909123420715),
                      (0.477272748947144, 1.0, 0.522727310657501),
                      (0.545454561710358, 1.0, 0.454545468091965),
                      (0.602272748947144, 1.0, 0.397727280855179),
                      (0.659090936183929, 1.0, 0.340909093618393),
                      (0.715909123420715, 1.0, 0.284090906381607),
                      (0.772727251052856, 1.0, 0.227272734045982),
                      (0.829545438289642, 1.0, 0.170454546809196),
                      (0.886363625526428, 1.0, 0.113636367022991),
                      (0.943181812763214, 1.0, 0.0568181835114956),
                      (1.0, 1.0, 0.0), (1.0, 0.9375, 0.0), (1.0, 0.875, 0.0),
                      (1.0, 0.8125, 0.0), (1.0, 0.75, 0.0), (1.0, 0.6875, 0.0),
                      (1.0, 0.625, 0.0), (1.0, 0.5625, 0.0), (1.0, 0.5, 0.0),
                      (1.0, 0.4375, 0.0), (1.0, 0.375, 0.0), (1.0, 0.3125, 0.0),
                      (1.0, 0.25, 0.0), (1.0, 0.1875, 0.0), (1.0, 0.125, 0.0),
                      (1.0, 0.0625, 0.0), (1.0, 0.0, 0.0),
                      (0.972039461135864, 0.0, 0.0),
                      (0.944078922271729, 0.0, 0.0), (0.916118443012238, 0.0, 0.0),
                      (0.888157904148102, 0.0, 0.0), (0.860197365283966, 0.0, 0.0),
                      (0.83223682641983, 0.0, 0.0), (0.804276287555695, 0.0, 0.0),
                      (0.776315808296204, 0.0, 0.0), (0.748355269432068, 0.0, 0.0),
                      (0.720394730567932, 0.0, 0.0), (0.692434191703796, 0.0, 0.0),
                      (0.664473652839661, 0.0, 0.0), (0.636513113975525, 0.0, 0.0),
                      (0.608552634716034, 0.0, 0.0), (0.580592095851898, 0.0, 0.0),
                      (0.552631556987762, 0.0, 0.0), (0.535087704658508, 0.0, 0.0),
                      (0.517543852329254, 0.0, 0.0), (0.5, 0.0, 0))
        self.colormap = ListedColormap(self._cmap)

    def create(self, time_seg, sensors=range(1, 37), title="HRM Plot", show=True):
        """
            Creates a spatio temporal plot of sensor data. Stores references to
            the figure and axes in corresponding class property.

            Arguments:
            ----------
            time_seg {iter} -- Paired data of start and stop of time segment.
            Can be SS.SS format or string format containing MM:SS.SS 

            sensors {iter int} -- Optional. Defaults to all 36 sensors. Iterable
            of integers corresponding to sensor number to be graphed. Each
            sensor will be graphed in its own subplot. 

            title {string} -- Title of the plot.

            show {bool} -- Optional. Determines whether the pyplot.show()
            command is called. If true the plot will be drawn, if false the plot
            will be created and can later be manipulated by accessing the figure
            properties.

            Returns:
            --------
            None
        """

        # Create shortcut for hrm.plot
        p = self.hrm.plot

        # Retrieve the data to be graphed
        try:
            p.Z, p.ann = self.hrm.get_segment(time_seg, sensors)
        except Exception as e:
            print("Could not segment the data.")
            return

        # Create the figure and axes objects.
        self.figure, self.axes = plt.subplots(1, 1, sharex=True,
                                              figsize=p.figsize)

        # Adjust the borders of the figure to remove extra whitespace but
        # include axes titles and plot titles.
        # rect=(left, bottom, right, top)
        # self.spatio_plot_fig.tight_layout(rect=(0.025, 0.02, 1.05, 0.96))

        # Plot the HRM data using imshow to create smoother color variation.
        self.image = self.axes.imshow(
            p.Z.T,
            interpolation="spline36",
            aspect="auto",
            cmap=self.colormap,
            vmin=-20,
            vmax=150)

        # Setup the colorbar
        cbar = self.figure.colorbar(self.image)
        cbar.set_label("Pressure (mmHg)", fontsize=p.fontsize)

        # Convert xtick labels based on time_in_mins property.
        self._conv_times(self.axes, "spatio")

        # Set the y-axis title
        plt.ylabel("Sensor Number", fontsize=p.fontsize)
        
        # Set the y-axis labels. The first tick must start at 0 but is labeled
        # with the first sensor number.
        yticks = range(0, len(sensors))
        plt.yticks(ticks=yticks, labels=sensors)

        # Set the overall figure title
        self.figure.suptitle(title, fontsize=p.fontsize+2)

        # If the show argument is true then show the figure
        if show:
            plt.show()

    def redraw(self):
        pass

    def draw_anns(self):
        # Create shortcut for hrm.plot
        p = self.hrm.plot
        ann_id = 1
        for idx, ann in p.ann.iterrows():
            x_position = ann.name
            x_position = np.where(p.Z.index.values == x_position)[0][0]
            text = ann["Text"]
            self.annotations.add(x_position, text, ann_id, show_label=True)
            ann_id += 1

    def remove_anns(self):
        pass
