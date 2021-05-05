from .plot import Plot
from .cimp import Import
from .data import Data
from . import ctime


class HRM():
    """
        This class serves as the base class for working with HRM data. Importing,
        plotting and manipulation of data occurrs using various subclasses.
    """

    def __init__(self):
        # Initialize the HRM class properties to their corresponding functional
        # classes. Pass self on initialization to permit the functional class
        # access to the data stored in the HRM base class.
        self.data = Data(self)
        self.import_data = Import(self)
        self.plot = Plot(self)

    def get_segment(self, time_seg, sensors):
        """
            This function segments the full HRM pressure data frame to only
            include the segment indicated by the input arguments. Can segment by
            both time and sensors.

            Arguments: 
            ----------
            time_seg {iter float | iter string} -- Must be paired given as
            either float or string. Can be in the format of (78.3, 82.1) or as
            ("1:18.3", "1:22.1")

            sensors {iter int} -- The sensors which to graph.

            Returns:
            --------
            Z {pandas data frame} -- Segment of df_HRM pressure data. Includes
            Time column as first column of data frame. Of shape (time,
            num_sensors). Index of table is the time in SS.SS.

            ann {pandas data frame} -- The annotation text and time that are
            within the time range of the segment. Of shape (time, 1). Index of
            table ins the time column and the annotation text is the only
            column.
         """

        # Check if any data has been loaded. If self.data.pressures is None,
        # getattr will return the default value of True.
        if getattr(self.data.pressures, "empty", True):
            raise Exception("No data has been loaded yet. Cannot segment.")

        # Create a copy as a list from the input time_seg and sensors.
        time_seg = list(time_seg)
        sensors = [int(i) for i in sensors]

        # Check to see if time_seg is a tuple or list, ensure it is length of 2
        # (paired data) and ensure the contained items are not tuples or lists,
        # then convert each of the times to float.
        time_start, time_end = self.process_time_seg(time_seg)

        # Select portion of the dataframe bewteen time segments
        p = self.data.pressures
        Z = p.loc[(p.index >= time_start) & (p.index < time_end), sensors]

        # Select the portion of the annotation dataframe that is between time
        # segments
        a = self.data.annotations
        ann = a.loc[(a.index >= time_start) & (a.index < time_end)]

        return Z, ann

    def process_time_seg(self, time_seg):
        """
            Processes the input time_seg. Checks to see if it is a pair of data
            stored in either an iterable with a pair of data. Ex: ('1:34.6',
            '1:42.2'). Can be a pair of strings or a pair of float numbers. Then
            converts any string numbers to floats using ctime module.

            Arguments:
            ----------
            time_seg {iter} -- Should be length of 2, either strings
            or floats.

            Returns:
            --------
            time_seg {list float} -- Converted time segment.
        """

        # Set the exception text
        ex_msg = "time_seg must be paired data. Ex: ('1:34.6', '1:42.2')"

        # Create a copy as a list from the input time_seg.
        time_seg = list(time_seg)

        # Check to see if time_seg is paried data of length 2.
        if len(time_seg) == 2:
            # Convert the tuples in time_seg to seconds.
            time_seg = ctime.time_in_sec(time_seg)
        else:
            raise Exception(ex_msg)

        return time_seg

    def save_to_text(self, save_path):
        """
            Saves the data currently stored in class properties df_HRM and
            df_ann to a text file. 

            Arguments:
                save_path {string} -- location of the new text file including
                name

            Returns:
                success {bool} -- whether or not the save operation completed
                successfully
        """
        success = False
        self.data.pressures.to_csv(save_path,
                           header=True,
                           index=False,
                           sep="\t",
                           mode="w")

        with open(save_path, "a") as file:
            file.write("Annotations:\n")

        sort = self.data.annotations.sort_values(["TIME"])
        sort.to_csv(save_path,
                    header=False,
                    index=False,
                    sep="\t",
                    mode="a")
        success = True

        return success

        
if __name__ == "__main__":
    h = HRM()
    h.import_data.from_text(
        r"D:\McCulloch Lab\Sleep Manometry Study\Subject 196, All Done.txt")
    h.plot.spatio.create((73, 75.4), title="Spatio Plot")
