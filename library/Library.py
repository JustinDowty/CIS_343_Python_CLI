import glob
import curses
import curses.textpad
import sys

class Library:
    """My library class only has two functions, and that is to change the directory listed and
       add a file to the playlist. These functions return the data that the Front End will load
       to screen."""
    def __init__(self):
        self.files = []   

    def getDirectoryFiles(self, path):
        """Get directory returns a list of files from a give path"""
        self.files = glob.glob(path)
        return self.files
		
