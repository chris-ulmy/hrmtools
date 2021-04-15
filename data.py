class Data():
    """
        This class serves as a storage object for HRM data. 
    """

    def __init__(self, hrm):
        self.hrm = hrm
        self.pressures = None
        self.annotations = None

    def __repr__(self):
        """
            String representation of the Data object. Gives shape of pressures
            dataframe and the number of annotations stored.
        """

        if getattr(self.pressures, "empty", None):
            # Retrieve the shape of the dataframe
            shape_p = self.pressures.shape
        else:
            shape_p = None
        if getattr(self.annotations, "empty", None):
            # Retrieve number of rows
            shape_a = self.annotations.shape[0]
        else:
            shape_a = None

        # Build the expression to return
        expression = (f"Data(pressures=pandas.dataframe of shape {shape_p}, "
                      + f"annotations=pandas.dataframe of shape {shape_a})")
        return expression

    def save_to_text(self, save_path):
        """
            Saves the data currently stored in data class property and
            in a new text file.

            Arguments:
            ----------
            save_path {string} -- location of the new text file including
            name.

            Returns:
            --------
            success {bool} -- whether or not the save operation completed
            successfully
        """

        try:
            # Save the HRM pressure data first text file.
            self.pressures.to_csv(save_path,
                                  header=True,
                                  index=False,
                                  sep="\t",
                                  mode="w")

            # Append Annotations: to the text file.
            with open(save_path, "a") as file:
                file.write("Annotations:\n")

            # Sort the annotations by Time
            sort = self.annotations.sort_values(["Time"])

            # Append the annotations to the output text file.
            sort.to_csv(save_path,
                        header=False,
                        index=False,
                        sep="\t",
                        mode="a")
        except Exception as e:
            print(f"{type(e)} Was not able to save the data as a text file.")
            success = False
            return success
        else:
            success = True
            return success
