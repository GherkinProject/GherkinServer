#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

#playing audio
import audio

#local lib : loading db
from load_db import *
import create_db

#thread
from threading import Thread

#config file
from configServer import *

#config file
from time import *
from random import randint

#Markov Process
from Markov import Markovienne

#http server
import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer



class ai:
    def __init__(self):
        #connection with audio
        self.audio = audio.server()

        #variable
        self.hist = []
        self.playlist = []
        self.songs = dict()
        self.point = 0
        self.mode = config.normal
        self.repeat = False

        #getting library
        self.get_lib()
        
        #Markov chain
        self.Markovienne = Markovienne(config.dbMarkov)

        try:
            self.Markovienne.load_Markov(config.dbMarkov)
        except:
            self.Markovienne.create_Markov(self.songs.keys())

#-------------------------------------------------------------------
#-------------------------------------------------------------------
#interface with ui
#-------------------------------------------------------------------
#-------------------------------------------------------------------

#----------------------------
#getters
#----------------------------

    def get_playlist(self):
        return self.playlist

    def get_point(self):
        if len(self.playlist) > 0:
            return self.point
        else:
            return None
    
    def get_db(self):
        with open(config.defaultDbLocation + config.defaultDbFile, "rb") as handle:
            return xmlrpclib.Binary(handle.read())

    def get_mode(self):
        return self.mode

    def get_repeat(self):
        return self.repeat

    def get_position(self):
        """return (int) the current position in the song ( in second )"""
        return self.audio.get_position()

    def get_duration(self):
        """return (int) the total duration of the song ( in second )"""
        return self.audio.get_duration()
   
    def is_playing(self):
        """Return the state of the audio player"""
        return self.audio.is_playing()

    def is_loaded(self):
        """Return the state of the audio player"""
        return self.audio.is_loaded()

    def get_name(self):
        """Return artist, album, track, name of song played"""
        if self.audio.is_loaded():
            return self.songs[self.playlist[self.point]]["artist"] + ", " + self.songs[self.playlist[self.point]]["album"] + ", " + str(self.songs[self.playlist[self.point]]["tracknumber"]) + ", " + self.songs[self.playlist[self.point]]["title"]
        else:
            return "No song loaded"

    def update_db(self, path):
        """Update the db according to the given path"""
        #cfgParse.set('location','DbLoc', %(path)s)
        create_db.thread_update_db(path, self.lastUpdate)

    def thread_update_db(self):
        pass

    def get_lib(self):
        (a, b, self.songs) = get_lib()
        self.lastUpdate = time()

    def get_root(self):
	return config.root
        
#----------------------------
#setters
#----------------------------

    def set_playlist(self, playlist):
        """Change playlist"""
        self.playlist = playlist

    def set_point(self, point):
        """Change pointeur of playlist position"""
        #update hist and point
        self.point = point
        try:
            self.hist.append((self.playlist[self.point], time()))
        except:
            pass

    def random(self):
        if self.mode == config.random:
            self.mode = config.normal
        
        else:
            if self.mode == config.playlist:
                self.Markovienne.save_Markov()
            
            self.mode = config.random

            #removing last elements from the playlist for it to be ready for next
            self.playlist = self.playlist[0:self.point+1]
    
    def mode_playlist(self):
        if self.mode == config.playlist:
            self.mode = config.normal
        
        else:
            self.mode = config.playlist

            #removing last elements from the playlist for it to be ready for next
            self.playlist = self.playlist[0:self.point+1]
    
    def mode_repeat(self):
        self.repeat = not self.repeat
    
#----------------------------
#audio actions
#----------------------------

    def change(self, point):
        """Lauch song pointed"""
        #change pointeur
        self.set_point(point)
       
        #we increase the probabily to go from idSongNow to idSong and decrease the other
        #we do a pruning of the successors of idSongNow
        
        #>>>>>>>>>>>>>>> why try: ? if no previous song played ? ok but 'if' works too...
        #we have to test if the
        try:
            self.Markovienne.vote_Markov(self.hist[-2][0], self.hist[-1][0])
            self.Markovienne.elagage(self.hist[-2][0], config.epsilon)
        except:
            pass

        self.load()
        self.play_pause()

    def next(self):
        #few things to do if we are in normal mode... just incrementing the pointeur
        if self.repeat:
            self.stop()
            self.load()
            self.play_pause()
        else:
            if self.mode == config.normal:
                if self.point < len(self.playlist) - 1:
                    self.set_point(self.point+1)
                    self.load()
                    self.play_pause()
                    return True
                else:
                    self.point = 0
                    self.stop()
                    return False
            else:
                if self.mode == config.random:
                    #choosing a random number in the list of possible song
                    posSong = randint(0, len(self.songs))
                    idSong = self.songs.keys()[posSong] 
                elif self.mode == config.playlist:
                    idSong = self.Markovienne.choix_Markov(self.playlist[self.point])
                
                #adding the song to the playlist
                self.playlist.append(idSong)
                
                #pointing on the new song
                self.set_point(self.point+1)
                
                #loading
                self.load()
                self.play_pause()

    def prev(self):
        #if we are not at the first element, no problem
        if self.point > 0:
            self.point -= 1
        else:
            self.point = len(self.playlist)-1
            
        self.load()
        self.play_pause()
        
        #erasing the lasts elements in those mode taking into account the user didn't like the music proposed
        if self.mode == config.playlist or self.mode == config.random:
            self.playlist.pop(-1)
        
    def play_pause(self):
        self.audio.play_pause()

    def stop(self):
        self.audio.stop()

    def get_volume(self):
        return self.audio.get_volume()

    def set_volume(self, vol):
        self.audio.set_volume(vol)

#-------------------------------------------------------------------
#-------------------------------------------------------------------
#internal function and methods
#-------------------------------------------------------------------
#-------------------------------------------------------------------

    def load(self):
        self.stop()
        self.audio.load(self.songs[self.playlist[self.point]]["location"])

def run(ai):
    while True:
        sleep(config.dtCheck)
        if ai.is_playing() and ai.get_position() > ai.get_duration() - config.anticipateCheck:
            while True:
                if ai.get_position() == ai.get_duration():
                    ai.next()
                    break

server = ai()
#thread
running = Thread(target = run, args = (server,))
running.setDaemon(True)
running.start()

# Create server
s = SimpleXMLRPCServer((config.serverName, config.defaultPort), logRequests = False, allow_none=True)
s.register_instance(server)

# Run the server's main loop
s.serve_forever() 
