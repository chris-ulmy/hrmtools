from collections import namedtuple
from collections.abc import MutableMapping
import pandas as pd


class Annotation():
    """
        Serves as a data storage object for annotation lines. Stores both the
        line object and the associated text label. 

        Configure whether the text box is drawn with show_labels property.
        Control the position of the text box with text_offset and label_y_offset
        properties.
    """

    def __init__(self, axes, x_position, text, ann_id,
                 show_label, text_offset, label_y_offset):
        self.axes = axes
        self.ann_id = int(ann_id)
        self.show_label = bool(show_label)
        # The offset of the text box from the annotation line in pixels?
        self.text_offset = float(text_offset)
        # The offset to draw the text box relative to the y-axis. Top of y-axis
        # is 1, bottom of y-axis is 0.
        self.label_y_offset = float(label_y_offset)
        self.line_obj = None
        self.text_obj = None
        self._label_y_position = None
        self._time_position = None
        self.create(x_position, text)

    def __repr__(self):
        """
            String representation of the current Annotation object.
        """
        expression = (f"Annotation(x_position={self.x_position}, "
                      f"line_obj={self.line_obj}, text_obj={self.text_obj}, "
                      f"show_label={self.show_label}, "
                      f"text_offset={self.text_offset}, "
                      f"label_y_offset={self.label_y_offset})")
        return expression

    @property
    def x_position(self):
        """
            Gets the x_position property. The value is retreived from the xdata
            property of the annotation line stored in the line_obj property.

            Arguments:
            ----------
            None

            Returns:
            --------
            x_position {float or int} -- Position on the x-axis to draw the
            line. Given in the x-axis data value.
        """

        # xdata stored as a list of len 2. To indicate each point of the line.
        return self.line_obj.get_xdata()[0]

    @x_position.setter
    def x_position(self, x_position):
        """
            Sets the x_position property. The value is stored within the xdata
            property of the annotation line stored in the line_obj property.

            Arguments:
            ----------
            x_position {float or int} -- Position on the x-axis to draw the
            line. Given in the x-axis data value.

            Returns:
            --------
            None
        """

        # x_position is duplicated to indicate x position of each point of the
        # line.
        self.line_obj.set_xdata([x_position] * 2)

    @property
    def label_y_position(self):
        """
            The get method for a property that cacluates the y_position of the
            labeling text based upon the label_y_offset property. Uses pyplot's
            transformation objects.

            Arguments:
            ----------
            None

            Returns:
            --------
            _label_y_position {float} -- The position on the y-axis on which to
            draw the text box label. In y-axis data format. 
        """

        # Create the transformer from axes scale (0 to 1) to display scale.
        transAxes = self.axes.transAxes

        # Transform the label_y_offset property to display scale.
        display = transAxes.transform((0, self.label_y_offset))

        # Create the inverted transformer to go from display scale to data
        # scale.
        transData = self.axes.transData.inverted()

        # Transform from display scale to data scale. Discard the x position.
        _, self._label_y_position = transData.transform(display)

        # Return the result.
        return self._label_y_position

    @property
    def time_position(self):
        """
            THIS MAY NOT WORK!!! NO access to Plot property anymore.
            The get method for a property that calculates the position in SS.SS
            of the annotation line. Converts from the x-position based on the
            spatiotemp plot's x-axis.
        """

        # Take the stored x_position propery, round and convert it an integer.
        # The x-position corresponds to the relative position on the
        # spatiotemp's x-axis.
        x_position = int(round(self.x_position, 0))

        # Set the hidden property to the time in SS.SS from the Plot.T property.
        # self._time_position = self.Plot.T[x_position]

        # Return the hidden property.
        return self._time_position

    def create(self, x_position, text):
        """
            Creates the line and text objects associated with the axes stored in the
            axes property. 

            Arguments:
            ----------
            x_position {float or int} -- the position on the x-axis to draw the
            annotation line.

            text {string} -- the text to associate with the annotation line.

            Returns:
            --------
            None
        """

        # Create the line object and store reference to in in the line_obj
        # property.
        self.line_obj = self.axes.axvline(x_position, color="r", picker=5)

        # If the show_label property is true, then create the text box and store
        # reference to it in the text_obj property.
        if self.show_label:
            self.text_obj = self.axes.text(x_position + self.label_y_offset,
                                           self.label_y_position,
                                           text,
                                           rotation=90,
                                           color="black",
                                           fontweight="bold",
                                           bbox={"color": "white", "alpha": 0.4})


class Annotations():
    """
        This class serves to store all annotation related objects when drawing
        HRM plots with pyplot. 

        It inherits from the MutableMapping abstract class. Stores Annotation
        objects in a dictionary whose keys are the axes object on which the
        annotation is drawn. 
    """

    def __init__(self, hrm):
        self.hrm = hrm
        self.table = None
        self._label_y_position = None
        self._time_position = None
        self.make_table()

    def __repr__(self):
        """
            String representation of the current Annotations object.
        """
        # Create return expression
        expression = f"Annotations object with annotations stored."

        return expression

    def __setitem__(self, key, value):
        """
        """
        pass

    def make_table(self):
        """
            Make a blank data table to store the annotations in.
        """

        self.table = pd.DataFrame(columns={"Axes": "object",
                                           "Text": "string",
                                           "Annotation": "object"},
                                  index={"Ann_ID": "int"})

    def add(self, x_position, text, ann_id, show_label=False, text_offset=6,
            label_y_offset=0.75):
        """
            Create on all axes in hrm
        """
        line_axes = getattr(self.hrm.plot.line, "axes", None)
        spatio_axes = getattr(self.hrm.plot.spatio, "axes", None)

        try:
            axes = [ax for row in line_axes for ax in row]
        except TypeError:
            axes = []

        if spatio_axes:
            axes.append(spatio_axes)

        for ax in axes:
            ann = Annotation(ax, x_position, text, ann_id, show_label,
                             text_offset, label_y_offset)
            new_row = pd.Series({"Axes": ax,
                                 "Text": text,
                                 "Annotation": ann},
                                name=ann_id)
            self.table.append(new_row)
            ann.create(x_position, text)
