import glob
import curses
import curses.textpad
import os
from .CLI_Audio_Exceptions import *

import sys

class FrontEnd:

    def __init__(self, player, library):
        """FrontEnd init initializes the curses screen in terminal, 
        checking that that screen size is large enough to contain application,
        init takes a player and library parameter that gets set to its own 
        Player and Library instance variables, an empty playlist array gets initialized,
        and lastly curses is initialized and menu is called within the curses wrapper context"""
        self.stdscr = curses.initscr()
        try:
            self.screen_height, self.screen_width = self.stdscr.getmaxyx()
            # I have determined these values to be approprite bounds for the screen size
            if(self.screen_height < 27 or self.screen_width < 130):
                raise CLI_Small_Screen_Exception
        except CLI_Small_Screen_Exception:
            print("ERROR: SCREEN SIZE TOO SMALL")
            self.quit()
        self.player = player
        self.library = library
        self.playlist = []
        self.files = []
        curses.wrapper(self.menu)
        

    def menu(self, args):
        """menu is the main input loop within the curses context, the screen is updated
        before entering the input loop, which calls other functions according to input"""
        self.resetScreen()
        self.updateSong()
        self.stdscr.refresh()
        while True:
            c = self.stdscr.getch()
            if c == 27:
                self.quit()
            elif c == ord('p'):
                self.player.pause()
            elif c == ord('c'):
                self.changeSong()
                self.updateSong()
                self.stdscr.touchwin()
                self.stdscr.refresh()
            elif c == ord('d'):
                self.changeDirectory()
                self.resetScreen()
                self.updateSong()
                self.updateDirectory()
                self.updatePlaylist()
            elif c == ord('s'):
                fileInDir = self.addFileToPlaylist()
                self.resetScreen()
                self.updateSong()
                self.updateDirectory()
                self.updatePlaylist()
                if not fileInDir:
                    # Printing error saying file not in directory
                    self.stdscr.addstr(17,10,"ERROR: NO FILE AT THAT PATH")
            elif c == ord('x'):
                self.playlist = []
                self.resetScreen()
                self.updateSong()
                self.updateDirectory()
    
    def updateSong(self):
        """updateSong changes the on screen display of current playing song"""
        self.stdscr.addstr(15,10, "                                        ")
        self.stdscr.addstr(15,10, "Now playing: " + self.player.getCurrentSong())

    def changeSong(self):
        """changeSong spawns a new curses window to prompt user for a new song path,
        once input is received it checks that the file exists, if it does the file will play
        via the Player instance, else an exception is thrown and a message printed"""
        changeWindow = curses.newwin(5, 30, 20, 10)
        changeWindow.border()
        changeWindow.addstr(0,0, "What is the file path?", curses.A_REVERSE)
        self.stdscr.refresh()
        curses.echo()
        path = changeWindow.getstr(1,1, 30)
        curses.noecho()
        del changeWindow
        self.stdscr.touchwin()
        self.stdscr.refresh()
        self.player.stop()
        try:
            #Checks if file exists, if not throw exception
            exists = os.path.isfile(path.decode(encoding="utf-8"))
            if not exists:
                raise CLI_File_Not_Found_Exception
            #If song exists error line is reset, then song is played
            self.stdscr.addstr(20,10,"                              ")
            self.player.play(path.decode(encoding="utf-8"))
        except CLI_File_Not_Found_Exception:
            self.stdscr.addstr(17,10,"ERROR: NO FILE AT THAT PATH")
        

    def quit(self):
        """quit ends curses and stops Player, exiting the application"""
        curses.endwin()
        #self.player.stop()
        exit()

    def resetScreen(self):
        """Resets the screen to original state, with no library or playlist displayed.
           This function does not clear the data saved regarding library and playlist, only resets the screen.
        when the screen is reprinted a write out of screen bounds exception is checked, this error should never
        happen since I control the maximum length of displayed file names below in updateDirectory and updatePlaylist"""
        self.stdscr.erase()
        self.stdscr.border()
        try:
            self.stdscr.addstr(0,0, "cli-audio",curses.A_REVERSE)
            self.stdscr.addstr(5,10, "c - Change current song")
            self.stdscr.addstr(6,10, "p - Play/Pause")
            self.stdscr.addstr(9,10, "ESC - Quit")
            self.stdscr.addstr(4,60, "LIBRARY")
            self.stdscr.addstr(4,100, "PLAYLIST")
            self.stdscr.addstr(5,60, "d - change directory")
            self.stdscr.addstr(5,100, "s - add song to playlist")
            self.stdscr.addstr(6,100, "x - clear playlist")
            self.stdscr.refresh()
        except curses.error:
            print("ERROR: WRITE OUT OF BOUNDS")
            self.quit()

    def updateDirectory(self):
        """Updates the screens directory with values from files
        Only the last 25 characters of the file name is displayed to avoid write out of bounds errors"""
        ctr = 10
        for f in self.files:
            self.stdscr.addstr(ctr, 60, f[-25:])
            ctr += 1
        self.stdscr.refresh()

    def updatePlaylist(self):
        """Updates the screens playlist with values from playlist
        Only the last 25 characters of the file name is displayed to avoid write out of bounds errors"""
        ctr = 10
        for p in self.playlist:
            self.stdscr.addstr(ctr, 100, p[-25:])
            ctr += 1
        self.stdscr.refresh()

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
        self.files = self.library.getDirectoryFiles(path)

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
            curses.noecho()
            self.playlist.append(newSong)
            return True
        else:
            curses.noecho()
            return False


