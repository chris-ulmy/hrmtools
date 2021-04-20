from line import Line
from spatio import Spatio


class Plot():
    """
        This class contains functions that handle the plotting of HRM data. Upon
        initilization it creates a link to the HRM "parent" object that stores
        the HRM data.
    """

    def __init__(self, hrm, time_in_min=False, figsize=(12, 10), fontsize=14):
        # Create link to HRM "parent" object
        self.hrm = hrm
        # Determines how the times are displayed. If true MM:SS.SS. If false
        # SS.SS
        self.time_in_min = time_in_min
        self.figsize = figsize
        self.fontsize = fontsize
        self.line = Line(hrm)
        self.spatio = Spatio(hrm)
        # self._config_path = r"E:\McCulloch Lab\PythonM\HRM\config.json"
        # self.anim = None
