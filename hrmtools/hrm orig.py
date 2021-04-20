# Imports
from cutools.HRM.plot import Plot
from cutools.HRM.cimp import Import
from cutools.HRM import ctime
import pandas as pd


class HRM():
    """
        This class serves as the base class for working with HRM data. Importing,
        plotting and manipulation of data occurrs using various subclasses.
    """

    def __init__(self):
        # Initialize the HRM class properties to their corresponding functional
        # classes. Pass self on initialization to permit the functional class
        # access to the data stored in the HRM base class.
        self.plot = Plot(self)
        self.import_data = Import(self)
        self.df_HRM = None
        self.df_ann = None

    def get_data_segment(self, time_seg, sensors=range(1, 37)):
        """
            This function segments the full df_HRM data frame to only include
            the segment indicated by the input arguments. Can segment by both
            time and sensors.

            Arguments:
            time_seg {tuple of float} or {tuple of string} -- Must be pair of
            of times given as either float or string.

            sensors {list of integers} -- Optional. Defaults to all 36 sensors.
            The sensors which to graph. Zero indexed.

            Returns:
            Z {pandas data frame} -- Segment of df_HRM pressure data, excluding
            time column. Of shape [num_sensors, time]. Note that the index for
            the row is not zero-indexed. Row number corresponds to actual sensor
            number.

            T {list of float} -- The corresponding times associated with the
            data segment.

            ann {pandas data frame} -- The annotation text and time that
            are within the time range of the segment.
         """

        # Check if any data has been loaded
        if isinstance(self.df_HRM, pd.DataFrame):
            if self.df_HRM.empty:
                Exception("No data has been loaded yet. Cannot segment.")
        elif not self.df_HRM:
            Exception("No data has been loaded yet. Cannot segment.")

        # Check to see if time_seg is a tuple or list, ensure it is length of 2
        # (paired data) and ensure the contained items are not tuples or lists,
        # then convert each of the times to float.
        time_seg = self.process_time_seg(time_seg)

        # Unpack time_seg
        time_start, time_end = time_seg

        # Select portion of the dataframe bewteen time segments
        Z = self.df_HRM[(self.df_HRM["TIME"] >= time_start) &
                        (self.df_HRM["TIME"] < time_end)]
        # Extract the time column, if needed for later use
        T = Z["TIME"].tolist()

        # Remove the time column
        Z = Z.drop(["TIME"], axis=1)

        # Convert sensors argument to list of strings in order to index Z
        sensors = [str(i) for i in sensors]

        # Select the sensor range to be graphed
        Z = Z[sensors]

        # Transpose the data
        Z = Z.T

        # Select the portion of the annotation dataframe that is between time
        # segments
        ann = self.df_ann[(self.df_ann["TIME"] >= time_start) &
                          (self.df_ann["TIME"] < time_end)]

        return Z, T, ann

    def process_time_seg(self, time_seg):
        """
            Processes the input time_seg. Checks to see if it is a pair of data
            stored in either a tuple or list. Ex: ('1:34.6', '1:42.2'). Can be a
            pair of strings or a pair of float numbers. Then converts any string
            numbers to floats using ctime module.

            Arguments:
            time_seg {tuple} or {list} -- Should be length of 2, either strings
            or floats.

            Returns:
            time_seg {list of float} -- Converted time seg of length 2.
        """

        # Set the exception text
        ex_msg = "time_seg must be paired data. Ex: ('1:34.6', '1:42.2')"

        # Check to see if time_seg is a tuple or list of length two and that
        # none of the members of that tuple/list are tuples or lists themselves.
        if (isinstance(time_seg, (tuple, list))
            and len(time_seg) == 2
            and not any([isinstance(time, (tuple, list))
                         for time in time_seg])):

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
        self.df_HRM.to_csv(save_path,
                           header=True,
                           index=False,
                           sep="\t",
                           mode="w")

        with open(save_path, "a") as file:
            file.write("Annotations:\n")

        sort = self.df_ann.sort_values(["TIME"])
        sort.to_csv(save_path,
                    header=False,
                    index=False,
                    sep="\t",
                    mode="a")
        success = True

        return success

# if __name__ == "__main__":
#     h = HRM()
#     h.import_data.from_text(
#         r"E:\McCulloch Lab\Sleep Manometry Study\Subject 120, All Done.txt")
