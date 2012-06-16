# -*- coding: utf-8 -*-
#!/usr/bin/python -d

#config constant

from configServer import *

#script with arguments
import sys

#client lib for calling server
import xmlrpclib


def give_time(u):
    if u % 60 < 10:
        return str(u // 60) + ":" + "0" + str(u % 60)
    else:
        return str(u // 60) + ":" + str(u % 60)

class client:
    def __init__(self):
        try:
            self.server = xmlrpclib.ServerProxy("http://" + config.serverName + ":" + str(config.defaultPort))
        except:
            assert False, "Server not launched !"
 
    
    def cmd(self, cmd):
        if cmd in "play" or cmd in "pause":
            self.server.play_pause()
        elif cmd in "next":
            self.server.next()
        elif cmd in "previous":
            self.server.prev()
        elif cmd in "state" or cmd in "display":
            r = ""
            if self.server.is_playing():
                r = r + "> "
            else:
                r = r + "|| "

            if self.server.get_repeat():
                r = r + "repeat "
             
            r = r + self.server.get_name() + " " + give_time(int(self.server.get_position())) + "/" + give_time(int(self.server.get_duration())) + " "

            if self.server.get_mode() == config.playlist:
                r = r + "ghk mode"

            print r
        
        elif cmd in "repeat":
            self.server.mode_repeat()

        elif cmd in "ghk" or cmd in "unghk":
            self.server.mode_playlist()

        elif cmd in "playlist":
            print self.server.get_playlist()

        elif cmd in "volume":
            try:
                self.server.set_volume(float(sys.argv[2]))
            except:
                print self.server.get_volume()
        else:
            print "Unknown command"
c = client()
#applying command
c.cmd(sys.argv[1])
