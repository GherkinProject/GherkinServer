#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

#standards libraries
#audio
import gst

#os
import os

#config file
from configServer import *

class server:
    def __init__(self):
        self.playing = False
        self.loaded = False
        #self.player = gst.Pipeline("player")
        self.player = gst.element_factory_make("playbin2", "player")
        fakesink = gst.element_factory_make("fakesink", "fakesink")
        self.player.set_property("video-sink", fakesink)
        
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)

 
    def load(self, path):
        """Load a song from the absolution or relative path "path" to the gstreamer audio server"""
        log.debug("Trying to load file " + path)
        if os.path.isfile(path):
            try:
                self.player.set_property("uri", "file://" + path)
            except:
                log.error("Gstreamer can't load file : " + path)
                self.loaded = False
                return False
            else:
                log.info("File " + path + " loaded")
                self.loaded = True
                return True
        else:
            log.error("Bad pathfile :" + path)
            return False

    def play_pause(self):
        """Play or pause the file if loaded, if not, do nothing"""
        if not self.playing:
            self.player.set_state(gst.STATE_PLAYING)
            self.playing = True
        else:
            self.player.set_state(gst.STATE_PAUSED)
            self.playing = False
    
    def stop(self):
        """De-load the file if loaded, compulsory if wanted to load a new file"""
        self.playing = False
        self.loaded = False
        self.player.set_state(gst.STATE_NULL)

    def get_position(self):
        """return (int) the current position in the song ( in second )"""
        if self.loaded:
            try:
                return round(self.player.query_position(gst.FORMAT_TIME, None)[0] / 1000000000., 1)
            except:
                return 0
        else:
            return -1

    def get_duration(self):
        """return (int) the total duration of the song ( in second )"""
        if self.loaded:
            try:
                return round(self.player.query_duration(gst.FORMAT_TIME, None)[0] / 1000000000., 1)
            except:
                return 100
        else:
            return -1
   
    def set_volume(self, vol):
        self.player.set_property("volume", vol) 

    def get_volume(self):
        return self.player.get_property("volume")

    def on_message(self, bus, message):
        """Print message sent by gstreamer"""
        t = message.type
        if t == gst.MESSAGE_EOS:
            self.player.set_state(gst.STATE_NULL)
            log.info("Reached end of file")
        elif t == gst.MESSAGE_ERROR:
            self.player.set_state(gst.STATE_NULL)
            err, debug = message.parse_error()
            log.error("Got gstreamer error : %s" % err, debug)
    
    def is_playing(self):
        """Return the state of the audio player"""
        return self.playing

    def is_loaded(self):
        """Return if a song is loaded in gstreamer"""
        return self.loaded
