from abc import ABC, abstractmethod
from matplotlib import pyplot as plt
from cutools.HRM import ctime


class Graph(ABC):
    """
        Abstract base class for creating graphs.
    """

    def __init__(self):
        self.figure = None
        self.axes = None

    @abstractmethod
    def create(self):
        """
            Creates a pyplot axes and figure. Stores references to them in
            corresponding class properties.
        """
        pass

    @abstractmethod
    def redraw(self):
        """
            Future capatability for animations and updating axes.
        """
        pass

    @abstractmethod
    def draw_anns(self):
        """
            Draw in the annotation markers on an existing axes.
        """
        pass

    @abstractmethod
    def remove_anns(self):
        """
            Remove annotation markers on an existing axes.
        """
        pass

    def _conv_times(self, axes, plot):
        """
            Converts the time_data to coincide with the time_in_min class
            property. If set to true, time_data will be converted to MM:SS.SS
            and x-axis label will adjust accordingly. If set to false, time_data
            will remain as SS.SS and x-axis label will adjust accordingly.

            Arguments:
            ----------
            axes {pyplot axes object} -- The axes from which to extract the
            current xtick label information.

            plot {string} -- Indicator as to whether a "spatio" or "line" is
            having its x-axis ticks adjusted.

            Returns:
            --------
            None
        """

        # Set pyplot to the current axes.
        plt.sca(axes)

        # Retrieve the current xticks values
        values, _ = plt.xticks()

        # Trim the first and last values. These are typically not shown by
        # pyplot regardless.
        values = values[1:-1]

        if self.hrm.plot.time_in_min:
            if plot == "spatio":
                # Convert the xtick labels of a spatio plot. This requires using
                # the current xtick values as indexes for the time index column
                # of the data segment stored in Z. Effectively gets the xtick
                # labels in SS.SS
                labels = [
                    self.hrm.plot.Z.index.values[int(idx)] for idx in values]

                # Convert the SS.SS xtick labels to MM:SS.S
                labels = ctime.time_in_min(labels)
            else:
                # Convert the xtick labels of a line plot. Values are already in
                # SS.SS
                labels = ctime.time_in_min(values)

            # Update the xticks with the new values and labels
            plt.xticks(values, labels)

            # Set the x-axis label
            axes.set_xlabel("Time (MM:SS.S)", fontsize=self.hrm.plot.fontsize)
        else:
            if plot == "spatio":
                # Use the current xtick vales as indexes for thet tiem index
                # column of the data segment stored in Z. Effectively gets the
                # xtick labels in SS.SS.
                labels = [
                    self.hrm.plot.Z.index.values[int(idx)] for idx in values]

                # Update the xticks with the new values and labels
                plt.xticks(values, labels)

            # Set the x-axis label
            axes.set_xlabel("Time (SS.SS)", fontsize=self.hrm.plot.fontsize)
