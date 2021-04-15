import PySimpleGUI as sg
import inspect


def open_file(func):
    """
        Private function used by cimp. Opens 
    """

    def open_file_inner(*args):
        print("opening file")
        file_path = args[1]
        if not file_path:
            file_path = sg.PopupGetFile("Choose a text file to open",
                                        title="Open",
                                        default_extension=".txt")

        with open(file_path) as file_obj:
            args = (args[0], file_obj)
            result = func(*args)
            return result
    return open_file_inner
