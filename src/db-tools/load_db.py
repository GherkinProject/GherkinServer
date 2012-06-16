#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

#standards libraries

#xml
import xml.etree.ElementTree as ET

#local libraries
from configServer import *

def get_lib(dbLocation = config.userLoc, dbFile = config.defaultDbFile):
    """Load songs dict from xml file"""
    tree = ET.ElementTree()
    tree.parse(dbLocation + dbFile)

    albumDict = {}
    artistDict = {}
    songs = {}
    for f in tree.findall('file'):
        #adding songs to the song libs ( with tags ) with an 'int' id
        id = f.get('id')
        songs[id] = {}
        songs[id]['id'] = id
        for element in f: 
            songs[id][element.tag] = element.get('value')
        
        if 'tracknumber' in songs[id].keys():
            try:
                tracknumber = int(songs[id]["tracknumber"].split("/")[0])
                songs[id]['tracknumber'] = tracknumber
            except:
                pass #bad tracknumber value

        #check if tags exist if not, putting unknown default value
        if 'title' not in songs[id].keys():
            songs[id]['title'] = songs[id]['location'].split('/')[-1]
        
        if 'artist' not in songs[id].keys():
            songs[id]['artist'] = config.defaultUnknown
        
        if 'album' not in songs[id].keys():
            songs[id]['album'] = config.defaultUnknown

        #adding dict to the graph if not existing
        if songs[id]['artist'] not in artistDict.keys():
            artistDict[songs[id]['artist']] = set()
        if songs[id]['album'] not in albumDict.keys():
            albumDict[songs[id]['album']] = set()


        #creating two dictionaries : artist -> albums: album -> tracks
        artistDict[songs[id]['artist']].add(songs[id]['album'])
        albumDict[songs[id]['album']].add(f.get('id'))

    log.info("Database loaded in memory")

    return (artistDict, albumDict, songs)

def make_neighbors(songs, tracks):
    """songs is the tag songs built up, songs is sth like graph[artist][album]"""
    
    #comparison function, used to sort tracks to make a decent playlist ( by artists/album/(track|name) )
    def comp(x, y):
        if songs[x]['artist'] > songs[y]['artist']:
            return +1
        elif songs[x]['artist'] < songs[y]['artist']:
            return -1
        else:
            if songs[x]['album'] > songs[y]['album']:
                return +1
            elif songs[x]['album'] < songs[y]['album']:
                return -1
            else:
                try:
                    if songs[x]['tracknumber'] > songs[y]['tracknumber']:
                        return +1
                    elif songs[x]['tracknumber'] < songs[y]['tracknumber']:
                        return -1
                    else:
                        return 0
                except:
                    if songs[x]['location'] > songs[y]['location']:
                        return +1
                    elif songs[x]['location'] < songs[y]['location']:
                        return -1
                    else:
                        return 0            

    playlist = list(tracks) #we have here a list of id's
    playlist.sort(comp) #we sort them
    
    return playlist
