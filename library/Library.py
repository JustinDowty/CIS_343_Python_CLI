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
           self.playlist = []     

    def changeDirectory(self):
        """Spawns a new window for the user to enter a new directory
           When a new directory is entered th screen is updated to contain the new directory's contents"""
        changeWindow = curses.newwin(5, 30, 20, 60)
        changeWindow.border()
        changeWindow.addstr(0,0, "What is the directory path?", curses.A_REVERSE)
        curses.echo()
        # Reformating path to contain wav files specifically 
        path = changeWindow.getstr(1,1, 30)
        path = path.decode(encoding="utf-8")
        path = path + "/*.wav"
        curses.noecho()
        self.files = glob.glob(path)
        return self.files

    def addFileToPlaylist(self):
        """Spawns a new window for the user to enter a valid file from the directory
           to add to their current playlist, playlist gets updated after file is chosen"""
        changeWindow = curses.newwin(5, 30, 20, 100)
        changeWindow.border()
        changeWindow.addstr(0,0, "Which song?", curses.A_REVERSE)
        curses.echo()
        newSong = changeWindow.getstr(1,1, 30)
        newSongDecode = newSong.decode(encoding="utf-8")
        if newSongDecode in self.files:
            self.playlist.append(newSong) 
        curses.noecho()
        del changeWindow
        return self.playlist
		
