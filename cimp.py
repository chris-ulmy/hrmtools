import pandas as pd
import PySimpleGUI as sg


class Import():
    """
        This class handles importing of HRM data. Upon initilization it creates a
        link to the HRM parent object that stores the HRM data.
    """

    def __init__(self, hrm):
        self.hrm = hrm

    def from_text(self, file_path):
        """
            This function imports HRM data from a txt file. The path to the txt
            file can be provided by the file_path arugment. If not it will be
            prompted by Windows file dialogue.

            Arguments: 
            ----------
            file_path {string} -- string that points to the txt file to be
            imported

            Returns: 
            --------
            df_HRM {pandas dataframe} -- dataframe containing all the HRM
            pressure data. The index of the dataframe is the time stamp. Each
            row is considered 1 time step. Each column is 1 pressure sensor
            (total of 36).

            df_ann {pandas.dataframe} -- dataframe containing all the
            annotations from the text file. The index of the dataframe is the
            time stamp. Each row is considered 1 time step. Single column
            contains the text of the annotation.
        """
        # Check if the file_path was given. If not, use a dialogue window to ask
        # the user for one.
        if not file_path:
            file_path = sg.PopupGetFile("Choose a text file to open",
                                        title="Open",
                                        default_extension=".txt")

        # Create the dtype input argument. The first two
        # columns must be objects as they contain text appended below the
        # pressure data in the form of the annotations. Sets all rest of the
        # columns to floats. Note the column names must be strings.
        data_dict = {"TIME": "object", "1": "object"}
        data_dict2 = {str(i): "float" for i in range(2, 37)}
        data_dict.update(data_dict2)

        # Read the entire csv file into a dataframe.
        try:
            df_full = pd.read_csv(file_path, delimiter="\t",
                                  dtype=data_dict)
        except Exception as e:
            print(f"{type(e)} The file was not able to be opened.")
            return

        # Rename the time column
        df_full = df_full.rename(columns={"TIME:": "Time"})

        # Determine the index of the row in which Annotations: appears.
        idx_of_ann = df_full[df_full["Time"] == "Annotations:"].index[0]

        # Copy out the rows that include Annotation data. Only need TIME and 1
        # columns.
        df_ann = df_full.loc[df_full.index > idx_of_ann, ("Time", "1")].copy()

        # Rename the second column
        df_ann = df_ann.rename(columns={"1": "Text"})

        # Convert Time column to float
        df_ann["Time"] = df_ann["Time"].astype("float")

        # Convert the Time column to the index for df_ann
        df_ann = df_ann.set_index("Time", drop=True)

        # Copy out the pressure data from df_full. Copy all rows greater than
        # the row starting Annotations.
        df_HRM = df_full.loc[df_full.index < idx_of_ann].copy()

        # Convert the Time and 1st sensor columns to float
        df_HRM[["Time", "1"]] = df_HRM[["Time", "1"]].astype("float")

        # Convert the Time column to the index for df_HRM
        df_HRM = df_HRM.set_index("Time", drop=True)

        # Convert the column names from strings to integers
        df_HRM.columns = range(1, 37)

        # Set the parent properties to the imported dataframes
        self.hrm.data.pressures = df_HRM
        self.hrm.data.annotations = df_ann

    def from_xml(self, file_path):
        """
            Function for future use to be able to import from xml files.
            Currently, only the annotations may be located within an xml file
            and not the HRM pressure data. Therefore, this is not used often and
            has not been completed as of yet.
        """
        pass
