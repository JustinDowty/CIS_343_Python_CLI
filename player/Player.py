"""PyAudio Example: Play a wave file (callback version)."""

import pyaudio
import wave
import time
import os
from ex.CLI_Audio_Exceptions import *

class Player:
    def __init__(self):
        self.currentSong = "Nothing playing."
        self.paused = True
        # Added this to be checked in stop function to avoid a "no member stream" error 
        # for running without a song playing at first
        self.stream = False
        self.position = 0

    def getCurrentSong(self):
        return self.currentSong

    def pause(self):
        if self.paused == False:
            self.paused = True
            self.stream.stop_stream()
        else:
            self.paused = False
            self.stream.start_stream()

    def play(self, track):
        self.paused = False
        self.currentSong = track
        #Checks if file exists, if not throw exception
        exists = os.path.isfile(track)
        if not exists:
            self.currentSong = "Nothing playing."
            raise CLI_File_Not_Found_Exception
        self.wf = wave.open(track, 'rb')
        # instantiate PyAudio (1)
        self.p = pyaudio.PyAudio()

        # open self.stream using callback (3)
        self.stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
                channels=self.wf.getnchannels(),
                rate=self.wf.getframerate(),
                output=True,
                stream_callback=self.callback)

        # start the self.stream (4)
        self.stream.start_stream()

    def stop(self):
        # Stop gets called before stream with the current implementation, 
        # Added this check to avoid error
        if(self.stream):
            self.stream.stop_stream()
            self.stream.close()
            self.wf.close()
            self.p.terminate()

    def callback(self, in_data, frame_count, time_info, status):
        data = self.wf.readframes(frame_count)
        return (data, pyaudio.paContinue)

