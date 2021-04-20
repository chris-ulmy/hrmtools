from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
from cutools.HRM import ctime
import PySimpleGUI as sg
import numpy as np
import json
from matplotlib import animation


class Annotations():
    """
    This class serves to store references to the annotaiton lines and
    annotation text. It provides a method of keeping the approprite line
    associated with its corresponding text element.
    """

    def __init__(self, plot):
        """
        This method initializes the Annotation object. It will create a
        reference to the Plot class that wil be used to retrieve plotting data.
        """

        # The Plot property is a reference to the parent plot class. This class
        # stores the plotting functions and data.
        self.Plot = plot
        self.axes = None
        self.x_position = None
        self.line = None
        self.text = None
        self.text_offset = 6
        self._label_y_position = None
        self._label_y_offset = 0.75
        self._time_position = None
        self.ann_idx = None
        self.show_labels = False

    @property
    def label_y_position(self):
        """
            The get method for a property that cacluates the y_position of the
            labeling text based upon the label_y_offset property.
        """

        # Determine the total number of sensors displayed by spatiotemp plot.
        total_sensors = len(self.Plot.spatio_sensors)

        # Caculates the y_position of the label based upon the label_y_offset.
        # Set the hidden property.
        self._label_y_position = int(self._label_y_offset * total_sensors)

        # Return the hidden property.
        return self._label_y_position

    @property
    def time_position(self):
        """
            The get method for a property that calculates the position in SS.SS
            of the annotation line. Converts from the x-position based on the
            spatiotemp plot's x-axis.
        """

        # Take the stored x_position propery, round and convert it an integer.
        # The x-position corresponds to the relative position on the
        # spatiotemp's x-axis.
        x_position = int(round(self.x_position, 0))

        # Set the hidden property to the time in SS.SS from the Plot.T property.
        self._time_position = self.Plot.T[x_position]

        # Return the hidden property.
        return self._time_position

    def add_from_segment(self, axes, ann_idx, show_labels=False):
        """
            This method will create a line object and text object and store them
            in the corresponding properties of the Annotation class based upon
            the given ann_idx provided as an input argument.

            Arguments: 
                axes {matplotlib axes object} -- Serves as the reference
                as to which axes the annotation belongs to.

                ann_idx {integer} -- The annotation index that corresponds to
                the indicies of the Plot.HRM.df_ann pandas dataframe.

                show_labels {boolean} -- Determines whether to show the label text
                or not associated with the annotation line.

            Returns:
                None
        """

        # Set the ann_idx property according to the input ann_idx
        self.ann_idx = ann_idx

        # Set the reference to the axes object
        self.axes = axes

        # Store the show_labels boolean input argument for later.
        self.show_labels = show_labels

        # Search the Plot.HRM.df_ann pandas dataframe for the TIME that
        # corresponds to the ann_idx
        time = self.Plot.HRM.df_ann.at[self.ann_idx, "TIME"]

        # Get the index of the Plot.T vector that stores the times in SS.SS
        # format. This index corresponds to the x-axis position to place the
        # line/text.
        self.x_position = self.Plot.T.index(time)

        # Create the line object at the x_position
        self.line = self.axes.axvline(self.x_position, color="r", picker=5)

        # If show_labels was indicated as true, also create the label text.
        if show_labels:
            # Search the Plot.HRM.df_ann pandas dataframe for the TEXT that
            # corresponds to the ann_idx
            text = self.Plot.HRM.df_ann.at[self.ann_idx, "TEXT"]

            # Create the text at the time_idx position + text_offset so as to
            # prevent line/text overlap. Also creates the text with a background
            # box to ensure text visibility.
            self.text = self.axes.text(self.x_position + self.text_offset,
                                       self.label_y_position,
                                       text,
                                       rotation=90,
                                       color="black",
                                       fontweight="bold",
                                       bbox={"color": "white", "alpha": 0.4})

    def move(self, x_position):
        """
            This method will move the matplot line object and its corresponding
            labelling text to a new x_position relative to the spatiotemp plot's
            x-axis position.

            Arguements: 
                x_position {float or int} -- The new x_position to draw the line
                and text at.

            Returns:
                None
        """

        # Round and convert the input x_position to an integer. Store it in the
        # x_position property.
        self.x_position = int(round(x_position, 0))

        # Set the line objects x position. xdata property stores a list of
        # length 2 so duplicate the x_position.
        self.line.set_xdata([self.x_position] * 2)

        # If there was a reference to the corresponding text object then move
        # that too.
        if self.text:
            self.text.set_x(self.x_position + self.text_offset)

    def get_artists(self):
        """
            This method returns the line and text objects stored in the class.

            Arguments:
                None

            Returns:
                self.line {matplotlib line} -- Reference to the line object.
                self.text {matplotlib text} -- Reference to the text object.
        """
        return self.line, self.text

    def remove(self):
        """
            This method removes the line and text objects via their inherent
            remove() methods and deletes the references to those objects.

            Arguments:
                None

            Returns:
                None
        """

        self.line.remove()
        if self.text:
            self.text.remove()
        del self.line
        del self.text


class Plot():
    """
        This class contains functions that handle the plotting of HRM data. Upon
        initilization it creates a link to the HRM "parent" object that stores
        the HRM data.
    """

    # Color map for HRM spatiotemporal plotting, constant, private
    _cmap = ((0.0, 0.0, 0.5625), (0.0, 0.0, 0.6171875), (0.0, 0.0, 0.671875),
             (0.0, 0.0, 0.7265625), (0.0, 0.0, 0.78125), (0.0, 0.0, 0.8359375),
             (0.0, 0.0, 0.890625), (0.0, 0.0, 0.9453125), (0.0, 0.0, 1),
             (0.0, 0.25, 1), (0.0, 0.5, 1), (0.0, 0.75, 1), (0.0, 1.0, 1),
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
             (1.0, 0.0625, 0.0), (1.0, 0.0, 0.0), (0.972039461135864, 0.0, 0.0),
             (0.944078922271729, 0.0, 0.0), (0.916118443012238, 0.0, 0.0),
             (0.888157904148102, 0.0, 0.0), (0.860197365283966, 0.0, 0.0),
             (0.83223682641983, 0.0, 0.0), (0.804276287555695, 0.0, 0.0),
             (0.776315808296204, 0.0, 0.0), (0.748355269432068, 0.0, 0.0),
             (0.720394730567932, 0.0, 0.0), (0.692434191703796, 0.0, 0.0),
             (0.664473652839661, 0.0, 0.0), (0.636513113975525, 0.0, 0.0),
             (0.608552634716034, 0.0, 0.0), (0.580592095851898, 0.0, 0.0),
             (0.552631556987762, 0.0, 0.0), (0.535087704658508, 0.0, 0.0),
             (0.517543852329254, 0.0, 0.0), (0.5, 0.0, 0))

    def __init__(self, HRM):
        # Create colormap based on the constant _cmap
        self.color_map = ListedColormap(self._cmap)
        # Create link to HRM "parent" object
        self.HRM = HRM
        self.spatio_plot_fig = None
        self.spatio_plot_axes = None
        self.spatio_image = None
        self.spatio_title = None
        self.spatio_show_ann = True
        self.spatio_show_ann_labels = True
        self.spatio_sensors = []
        self.line_plot_fig = None
        self.line_plot_title = None
        self.line_plot_data_lines = []
        self.line_plot_sensors = []
        self.line_plot_show_ann = False
        self.line_plot_show_ann_labels = False
        self.Z = None
        self.T = None
        self.ann = None
        self.times_in_min = False
        self.show_ann = False
        self.show_ann_labels = False
        self.ann_obj = []
        self.line_plot_axes = []
        # self._spatio_plot_size_inch = ()
        # self._line_plot_size_inch = ()
        self._config_path = r"E:\McCulloch Lab\PythonM\HRM\config.json"

        self.anim = None

    # @property
    # def spatio_plot_size_inch(self):
    #     if not self._spatio_plot_size_inch:
    #         with open(self._config_path) as cfg:
    #             data = json.load(cfg)
    #             width = data.get("spatio_plot_size.width")
    #             scale = data.get("spatio_plot_size.height_scaling_factor")
    #             height = width / scale
    #             self._spatio_plot_size_inch = (width, height)

    #     return self._spatio_plot_size_inch

    # @property
    # def line_plot_size_inch(self):
    #     if not self._line_plot_size_inch:
    #         with open(self._config_path) as cfg:
    #             data = json.load(cfg)
    #             scale = data.get("line_plot_size.width_scaling_factor")
    #             line_plot_height = data.get("line_plot_size.height")
    #             spatio_width, _ = self.spatio_plot_size_inch
    #             line_plot_width = round(spatio_width / scale, 1)
    #             self._line_plot_size_inch = (line_plot_width, line_plot_height)

    #     return self._line_plot_size_inch

    def draw_spatio(self, sensors=range(1, 37),
                    times_in_min=True, figsize=None):
        """
            This function plots a spatiotemporal plot of the HRM data define
            through the input arguments. A specific time point can be chosen as
            well as specific sensors. The plot is stored as a figure object in
            in the spatio_plot_fig property.

            Arguments: 
                time_seg {tuple of strings} or {list of strings} -- The
                time segment given in a tuple pair or list pair (start_time,
                end_time). Example: ("1:34.6", "1:42.2").

                sensors {list of integers} -- Optional. The sensors which the
                spatiotemporal plot will include. Default is all 36 sensors.

                times_in_min {boolean} -- Optional. If set to true, the 
                x-tick markers will be displayed in MM.SS. If set to false,
                will display in SS.SS

                figsize {tuple of integers} -- Optional. Determines the size of the
                spatio plot. If left as None will use default plot size in pyplot.

            Returns:
                pyplot figure stored in the spatio_plot_fig class property.
        """
        self.spatio_sensors = sensors
        self.times_in_min = times_in_min
        num_sensors = len(self.spatio_sensors)

        # Extracts the segment and saves Z, T, and ann as class properties.
        # self.extract_segment(time_seg, self.spatio_sensors)

        # Create the figure and axes
        (self.spatio_plot_fig,
            self.spatio_plot_axes) = plt.subplots(1, 1,
                                                  figsize=figsize)

        # self.spatio_xaxis = self.spatio_plot_axes.xaxis
        # self.spatio_xaxis.set_animated(True)

        # Adjust the borders of the figure to remove extra whitespace but
        # include axes titles and plot titles.
        # rect=(left, bottom, right, top)
        self.spatio_plot_fig.tight_layout(rect=(0.025, 0.02, 1.05, 0.96))

        # Set the figure title
        self.spatio_title = self.spatio_plot_axes.set_title("")

        # Set the x-axes labels
        if self.times_in_min:
            # x-labels in MM:SS.SS. Change the x-axis title
            # coincide.
            x_label = "Time (MM:SS.SS)"
        else:
            # x-labels in SS.SS. Change the x-axis title coindide.
            x_label = "Time (sec)"
        plt.xlabel(x_label)

        # Setup the y-axis
        plt.ylabel("Sensor Number")
        self.draw_yticks(self.spatio_plot_axes)

        # Plot the HRM data using imshow to create smoother color
        # variation.
        self.spatio_image = self.spatio_plot_axes.imshow(
            np.random.random((num_sensors, self.Z.shape[1])) * 150,
            interpolation="spline36",
            aspect="auto",
            cmap=self.color_map,
            vmin=-10,
            vmax=150,
            animated=True)

        # Setup the colorbar
        cbar = self.spatio_plot_fig.colorbar(self.spatio_image)
        cbar.set_label("Pressure (mmHg)")

    def update_spatio(self, time_seg, title="HRM Plot",
                      show_ann=False,
                      show_ann_labels=False):
        """
            Redraws the spatiotemporal plot that was created in spatiotemp()
            function. This speeds up the redraw process without having to redo
            draw the entire plot each time.

            Arguments:
            time_seg {tuple of string or float} or {list of string or
            float} -- The time segment given in a tuple pair or list pair
            (start_time, end_time). Example: ("1:34.6", "1:42.2").

            sensors {list of integers} -- Optional. The sensors which the
            spatiotemporal plot will include. Default is all 36 sensors.

            Returns:
            pyplot figure stored in the spatio_plot_fig class property.
        """

        self.spatio_show_ann = show_ann
        self.spatio_show_ann_labels = show_ann_labels

        # Extracts the segment and saves Z, T, and ann as class properties.
        self.extract_segment(time_seg, self.spatio_sensors)

        # Plot the HRM data using imshow to create smoother color
        # variation.
        self.spatio_image.set_data(self.Z)

        self.spatio_title.set_text(title)

        # Set the x-axes tick marks. Save the times_in_min in the
        # times_in_min class property to remember for redraw method calls.
        self.draw_xticks(self.spatio_plot_fig)

        # Show annotation lines if present in the time_seg and if indicated
        # by argument show_ann. Save the show_ann in the show_ann class
        # property to remember for redraw method calls.
        if self.spatio_show_ann:
            self.delete_ann_axes(self.spatio_plot_axes)
            self.draw_ann(self.spatio_plot_axes, "spatio")

    def save_ann_positions(self):
        # axes_objects = self.axes_obj.get(self.spatio_plot_axes)
        # if axes_objects:
        #     # save them
        #     lines = axes_objects.get("lines")
        #     ann_idx = axes_objects.get("ann_idx")
        #     assert(len(ann_idx) == len(lines))
        #     for idx, line in zip(ann_idx, lines):
        #         x_position = int(round(line.get_xdata()[0], 0))
        #         new_time = self.T[x_position]
        #         self.HRM.df_ann.at[idx, "TIME"] = new_time

        ann_objs = [annotation for annotation in self.ann_obj
                    if annotation.axes == self.spatio_plot_axes]

        for annotation in ann_objs:
            new_time = annotation.time_position
            self.HRM.df_ann.at[annotation.ann_idx, "TIME"] = new_time

    def draw_ann(self, axes, plot_name):
        """
            Draws the annotation lines and corresponding text on the figure
            stored in spatio_plot_fig class property. Adds each line and text to the
            ann_lines and ann_texts properties respectively to keep track of
            them for later deletion.

            Arguments:
            fig_num {integer} -- The figure number from the pyplot.figure.number
            property.

            Returns:
            None
        """

        # lines = []
        # texts = []
        ann_idx = []

        existing_ann_idx = [
            ann.ann_idx for ann in self.ann_obj if ann.axes == axes]
        # Iterate through the rows of the ann data frame.
        for idx, row in self.ann.iterrows():
            # Extract TIME and TEXT from the row.
            # time = row["TIME"]
            # text = row["TEXT"]
            if not any(idx == ann_idx for ann_idx in existing_ann_idx):
                annotation = Annotation(self)
                if plot_name == "spatio":
                    annotation.add_from_segment(
                        axes, idx, self.spatio_show_ann_labels)
                elif plot_name == "line":
                    annotation.add_from_segment(
                        axes, idx, self.line_plot_show_ann_labels)
                self.ann_obj.append(annotation)
            # Get the index of the T vector that stores all time positions for
            # the dataset. This index corresponds to the x-axis position to
            # place the line/text.
            # time_idx = self.T.index(time)

            # Create the vertical line at the time_idx position.
            # line = axes.axvline(time_idx, color="r", picker=5, gid=str(idx))

            # lines.append(line)
            # ann_idx.append(idx)

            # if show_labels:
            #     # Create the text at the time_idx position + 6 so as to prevent
            #     # line/text overlap.
            #     text = axes.text(time_idx + 7, self.ann_txt_position, text,
            #                      rotation=90, color="black",
            #                      fontweight="bold",
            #                      bbox={"color": "white", "alpha": 0.4},
            #                      gid=str(idx))
            #     texts.append(text)

        # axes_objects_new = {"lines": lines, "texts": texts, "ann_idx": ann_idx}
        # self.axes_obj[axes] = axes_objects_new

    def delete_ann(self, ann_idx):
        idx_to_remove = []
        for idx, annotation in enumerate(self.ann_obj):
            if annotation.ann_idx == ann_idx:
                annotation.remove()
                idx_to_remove.append(idx)

        for idx in sorted(idx_to_remove, reverse=True):
            del self.ann_obj[idx]

    def delete_ann_axes(self, axes):
        """
            Deletes the annotation line and texts stored in the ann_lines and
            ann_texts class properties. Makes way for drawing new annotations.

            Arguments:
            None

            Returns:
            None
        """
        idx_to_remove = []
        for idx, annotation in enumerate(self.ann_obj):
            if annotation.axes == axes:
                annotation.remove()
                idx_to_remove.append(idx)

        for idx in sorted(idx_to_remove, reverse=True):
            del self.ann_obj[idx]

    def delete_ann_all(self):
        for annotation in self.ann_obj:
            annotation.remove()
        self.ann_obj = []

    def draw_xticks(self, fig, steps_between_ticks=7):
        """
            Reconfigures the x-axis tick marks to display the labels formatted
            in MM:SS.SS or SS.SS format, depending on the times_in_min class
            property. Can set the number of ticks to display.

            Arguments:
            fig_num {integer} -- The figure number from the pyplot.figure.number
            property.

            num_ticks_to_display {int} -- Optional. The number of tick marks to
            display on the x-axis.

            Returns:
            None
        """

        # Calculate the step or interval over which to jump through the t
        # vector. Converted to int to cut off any decimal points.
        step = int(len(self.T) / steps_between_ticks)

        # Get a list of the indexes that corresponds to the
        # num_ticks_to_display. This list will be the position on the x-axis
        # which to place the tick marks.
        T_positions = range(0, len(self.T), step)

        # Create the labels for the x-axis. Check if times_in_min is desired.
        if self.times_in_min:
            # Convert the labels to MM:SS.SS format.
            T_labels = [ctime._convert_to_min(
                self.T[index]) for index in T_positions]
        else:
            # Don't convert. Keep as raw SS.SS format.
            T_labels = [self.T[index] for index in T_positions]

        # Set the figure to be altered as the active figure
        plt.figure(fig.number)

        # Add the tick marks and their corresponding tick labels.
        plt.xticks(T_positions, T_labels, fontsize=10)

    def draw_yticks(self, axes):
        num_sensors = len(self.spatio_sensors)
        sensor_start = self.spatio_sensors[0]
        sensor_end = self.spatio_sensors[-1]
        axes.set_yticks(range(0, num_sensors))
        axes.set_yticklabels(range(sensor_start, sensor_end + 1), fontsize=10)

    def draw_line_plot(self, sensors=range(1, 37), title="Sensor Plots",
                       times_in_min=True, figsize=None):
        """

        """

        # Save show_ann in class properties for later use during redraws.
        self.times_in_min = times_in_min
        self.line_plot_sensors = sensors

        # Determine how many sensors will be plotted and how large to make
        # the plot
        num_sensors = len(sensors)
        # line_plot_width, line_plot_height = self.line_plot_size_inch
        # line_plot_height = plot_height * num_sensors  # in inches

        # Create the figure. Number of subplots = num_sensors. line_plot_axes is
        # an object array of the axes created.
        (self.line_plot_fig,
            self.line_plot_axes) = plt.subplots(num_sensors, 1,
                                                figsize=figsize,
                                                sharex=True)

        # If only one sensor was graphed, convert the line_plot_axes object into
        # a list so that it can be iterated over later.
        if num_sensors == 1:
            self.line_plot_axes = [self.line_plot_axes]

        # Adjust the borders of the figure to remove extra whitespace but
        # include axes titles and plot titles.
        # rect=(left, bottom, right, top)
        self.line_plot_fig.tight_layout(rect=(0.01, 0.02, .97, 0.96))

        # Set the figure title
        self.line_plot_title = self.line_plot_fig.suptitle(title)

        # Set the axes labels
        if self.times_in_min:
            # x-labels in MM:SS.SS. Change the x-axis title
            # coincide.
            x_label = "Time (MM:SS.SS)"
        else:
            # x-labels in SS.SS. Change the x-axis title coindcide.
            x_label = "Time (sec)"
        plt.xlabel(x_label)

        self.line_plot_data_lines = []
        t0 = self.T[0]
        x = [int((i-t0)*100) for i in self.T]
        y = np.ones((1, len(self.T))).tolist()[0]
        for axes, sensor in zip(self.line_plot_axes, self.line_plot_sensors):
            axes.margins(0, 0.25)
            axes.axhline(y=0, linestyle="--", color="black", alpha=0.25)
            line = axes.plot(x, y)[0]
            y_label = f"Sensor {str(sensor)}"
            axes.name = y_label
            axes.set_ylabel(y_label)
            self.line_plot_data_lines.append(line)

    def update_line_plot(self, time_seg, title="Sensor Plots",
                         show_ann=False,
                         show_ann_labels=False):
        """
            This
        """

        self.show_ann = show_ann
        self.show_ann_labels = show_ann_labels

        def animate_line_plot(i):
            artists = []
            assert(len(self.line_plot_data_lines)
                   == len(self.line_plot_data_lines)
                   == len(self.line_plot_sensors))
            line_plot_objs = zip(self.line_plot_axes,
                                 self.line_plot_data_lines,
                                 self.line_plot_sensors)
            t0 = self.T[0]
            x = [int((i-t0)*100) for i in self.T]
            for axes, line, sensor in line_plot_objs:
                y = self.Z.loc[str(sensor)].tolist()
                line.set_data(x, y)
                y_range = abs(max(y)) - min(y)
                y_max = round(max(y) + y_range * 0.25, 2)
                y_min = round(min(y) - y_range * 0.25, 2)
                axes.set_ylim(y_min, y_max)
            if not title == "Sensor Plots":
                self.line_plot_title.set_text(title)
            self.draw_xticks(self.line_plot_fig)
            return (self.line_plot_data_lines
                    + [self.line_plot_title])

        # Extracts the segment and saves Z, T, and ann as class properties.
        self.extract_segment(time_seg, self.line_plot_sensors)

        anim = animation.FuncAnimation(fig=self.line_plot_fig,
                                       func=animate_line_plot,
                                       interval=100,
                                       frames=1,
                                       repeat=False,
                                       blit=False)
        self.line_plot_fig.canvas.draw()

        # Show annotation lines if present in the time_seg and if indicated
        # by argument show_ann. Save the show_ann in the show_ann class
        # property to remember for redraw method calls.
        if self.show_ann:
            for axes in self.line_plot_axes:
                self.delete_ann_axes(axes)
                self.draw_ann(axes, "line")

    # def _line_plot_data(self, time_seg, sensors, first_draw=True):
        # if time_seg == "cache":
        #     # Use the same data in Z, T, and ann class properties.
        #     pass
        # else:
        #     # Extracts the segment and saves Z, T, and ann as class properties.
        #     time_start, time_end = self.extract_segment(time_seg, sensors)

        #     # Create the plots by looping over the sensors. sensors corresponds
        #     # to the index of the row in the Z dataframe
        #     for axes_num in range(num_sensors):
        #         sensor = sensors[axes_num]
        #         self._draw_line_plot_axes(axes_num, sensor)

    # def _draw_line_plot_axes(self, axes_num, sensor):
    #     sensor_data = self.Z.loc[str(sensor)].tolist()
    #     if isinstance(self.line_plot_axes, np.ndarray):
    #         axes = self.line_plot_axes[axes_num]
    #     else:
    #         axes = self.line_plot_axes

    #     plt.sca(axes)
    #     plt.cla()
    #     axes.plot(sensor_data)

    #     if self.show_ann:
    #         self.draw_ann(axes, show_labels=False)

    def extract_segment(self, time_seg, sensors=range(1, 37)):
        completed = False

        # Check to see if time_seg is a tuple or list, ensure it is length of 2
        # (paired data) and ensure the contained items are not tuples or lists,
        # then convert each of the times to float.
        if not time_seg == "cache":
            # time_seg = self.HRM.process_time_seg(time_seg)

            # Unpack time_seg
            # time_start, time_end = time_seg

            # Retrieve the desired segment of df_HRM and store the output in the
            # corresponding class properties
            self.Z, self.T, self.ann = self.HRM.get_data_segment(
                time_seg, sensors)

       # If one of the above inputs is outside of the dataframe range, warn
        # the user
        if self.Z.empty:
            sg.popup("The time segment input was not within bounds of a the ",
                     "HRM dataset.",
                     keep_on_top=True,
                     no_titlebar=True)
        else:
            completed = True

        return completed
