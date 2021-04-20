from .graph import Graph
from .ann import Annotations
from matplotlib import pyplot as plt
import numpy as np


class Line(Graph):
    """
        Inherits from Graph abstract base class. Creates a line plot using
        pyplot. 
    """

    def __init__(self, hrm):
        self.hrm = hrm
        self.annotations = Annotations(hrm)

    def create(self, time_seg, sensors=range(1, 37), title="HRM Plot"):
        """
            Creates a line plot of sensor data. Creates one axes for each sensor
            provided in sensors argument. Stores references to the figure and
            axes in corresponding class property.

            Arguments:
            ----------
            time_seg {iter} -- Paired data of start and stop of time segment.
            Can be SS.SS format or string format containing MM:SS.S 

            sensors {iter int} -- Optional. Defaults to all 36 sensors. Iterable
            of integers corresponding to sensor number to be graphed. Each
            sensor will be graphed in its own subplot. 

            title {string} -- Title of the plot.

            Returns:
            --------
            None
        """

        # Create shortcut for hrm.plot
        p = self.hrm.plot

        # Retrieve the data to be graphed
        p.Z, p.ann = self.hrm.get_segment(time_seg, sensors)

        # Determine the number of sensors to graph
        num_sensors = len(sensors)

        # Create the figure and axes objects. Create the number of subplots
        # based on the count of sensors. Shape of plot = (num_sensors, 1).
        self.figure, self.axes = plt.subplots(num_sensors, 1, sharex=True,
                                              figsize=(p.figsize))

        # Loop through the sensors and plot the data
        for idx, sensor in enumerate(sensors):
            # Retieve the axes to graph the data on
            if type(self.axes) == np.ndarray:
                axes = self.axes[idx]
            else:
                axes = self.axes

            # Retrieve a single column of the sensor data
            data = p.Z[sensor]

            # Plot the data. Use the index of the pandas dataframe stored in Z
            # as the x labels (time).
            axes.plot(p.Z.index.values, data)

            # If set to 0 will remove the added whitespace on either side of the
            # x-axis
            # axes.margins(x=0)

            # Set the title of the axes
            axes.set_title(f"Sensor {sensor}", fontsize=p.fontsize)

        # Convert xtick labels based on time_in_mins property. Only pass the
        # last axes which will be labeled accordingly.
        self._conv_times(self.axes[num_sensors-1], "line")

        # Create a blank subplot that surrounds the axes. Used to get the common
        # y-lable to show properly.
        self.figure.add_subplot(111, frameon=False)

        # Hide the tick marks of the blank subplot.
        plt.tick_params(labelcolor="none", top=False,
                        bottom=False, left=False, right=False)

        # Set the y-axis title
        plt.ylabel("Pressure (mmHg)", fontsize=p.fontsize)

        # Set the overall figure title
        self.figure.suptitle(title, fontsize=p.fontsize+2)

        # Show the figure
        plt.show()

    def create_overlay(self, time_seg, sensors=range(1, 37), title="HRM Plot"):
        """
            Creates a single axes with all sensors graphed over each other.

            Arguments:
            ----------
            time_seg {iter} -- Paired data of start and stop of time segment.
            Can be SS.SS format or string format containing MM:SS.S 

            sensors {iter int} -- Optional. Defaults to all 36 sensors. Iterable
            of integers corresponding to sensor number to be graphed. Each
            sensor will be graphed on the same axes. 

            title {string} -- Title of the plot.

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
            return

        # Create the figure and axes objects. Shape of plot = (1, 1).
        self.figure, self.axes = plt.subplots(1, 1, sharex=True,
                                              figsize=p.figsize)

        # Plot the data. Use the index of the pandas dataframe stored in Z
        # as the x labels (time).
        self.axes.plot(p.Z.index.values, p.Z)

        # Draw 0 line
        self.axes.axhline(y=0, linestyle="dashed", color="black", alpha=0.5)

        # Convert time data based on times_in_mins property. Only pass the last
        # axes which will be labeled accordingly.
        self._conv_times(self.axes, "line")

        # Set the y-axes titles of the figure
        plt.ylabel("Pressure (mmHg)", fontsize=p.fontsize)

        # Set the overall figure title
        self.figure.suptitle(title, fontsize=p.fontsize+2)

        # Create legend labels
        legend = [f"Sensor {sensor}" for sensor in sensors]

        # Turn on the legend
        self.axes.legend(legend, fontsize=p.fontsize)

        # Show the figure
        plt.show()

    def redraw(self):
        pass

    def draw_anns(self):
        pass

    def remove_anns(self):
        pass
