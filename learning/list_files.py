#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

#standards libraries

#xml
import xml.etree.ElementTree as ET

#local libraries
from configServer import *
import codecs

def get_dirs(dbLocation = config.defaultDbLocation, dbFile = config.defaultDbFile):
    """Load songs dirs from xml file"""
    tree = ET.ElementTree()
    tree.parse(dbLocation + dbFile)

    dirs = []
    for f in tree.findall('file'):
        dirs.append(f.find('location').get('value'))

    return dirs

def get_dirs2file(dbLocation = config.defaultDbLocation, dbFile = config.defaultDbFile):
    dirs = get_dirs(dbLocation, dbFile)
    with codecs.open('dirs.txt', 'w', 'utf-8') as f: 
        f.writelines(["%s\n" % item for item in dirs])



get_dirs2file()
