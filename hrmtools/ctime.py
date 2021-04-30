def time_in_sec(input_time):
    """
        Converts input_time from format MM:SS.SS to SS.SS

        Arguments: 
        input_time {string} or {list of string} -- string(s) with time
        given in MM:SS.SS

        Returns: 
        seconds {float} or {list of float} -- converted time in SS.SS
    """

    # Initialize output seconds
    seconds = []

    # Check if input_time was a string or a list of strings
    if isinstance(input_time, str):
        for t in input_time:
            seconds.append(sum(float(x) * 60 ** i for i, x in enumerate(reversed(t.split(':')))))
    elif isinstance(input_time, (list, tuple)):
        # Loop through the list or tuple.
        for time in input_time:
            seconds.append(_convert_to_sec(time))

    return seconds


def time_in_min(input_time):
    """
        Converts input_time from format SS.SS to MM:SS.S

        Arguments: 
        input_time {float} or {list of float} -- float(s) with time
        given in SS.SS

        Returns: 
        string {string} or {list of strings} -- converted time in MM:SS.S
    """

    # Initialize output seconds
    string = []

    # Check if input_time was a string or a list of strings
    if isinstance(input_time, float):
        string = _convert_to_min(input_time)
    else:
        input_time = list(input_time)
        # Loop through the list of strings
        for time in input_time:
            string.append(_convert_to_min(time))

    return string


def _convert_to_sec(input_time):
    """
        This function takes the input_time singular string and converts it from
        MM:SS.SS to SS.SS. If already in SS.SS will return a float in SS.SS
        format.

        Arguments: 
        input_time {string} -- string in the form of MM:SS.SS

        Returns: 
        seconds {float} -- converted MM to seconds and added to remainder
        seconds
    """

    # Check to see if a colon (":") was contained in input_time
    if isinstance(input_time, str) and ":" in input_time:
        # Split the string at the colon
        mins, secs = input_time.split(":")
        seconds = float(mins) * 60 + float(secs)
    else:
        # time is less than 1 minute
        seconds = float(input_time)

    return seconds


def _convert_to_min(input_time):
    """
        This function takes the input_time as a singular float number and
        converts it from SS.SS to MM:SS.S

        Arguments: 
        input_time {float} -- float in the form of SS.SS

        Returns: 
        string {string} -- string converted to MM:SS.S
    """

    # Check to see if input_time was a float
    if isinstance(input_time, float):
        # Convert to int first to remove decimal, then to string
        mins = str(int(input_time / 60))
        sec = str(round(input_time % 60, 2))
        string = mins + ":" + sec

    return string
