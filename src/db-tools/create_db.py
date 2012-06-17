#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

#standards libraries

#script with arguments
import sys

#script using system commands
import os

#time lin
from time import *

#thread
from threading import Thread

#script using dom
from xml.dom.minidom import Document
from xml.dom import minidom

#patch dom to gain space
def newwritexml(self, writer, indent= '', addindent= '', newl= ''):
    if len(self.childNodes)==1 and self.firstChild.nodeType==3:
        #writer.write(indent)
        self.oldwritexml(writer) # cancel extra whitespace
        #writer.write(newl)
    else:
        self.oldwritexml(writer, indent, addindent, newl)
oldwritexml = minidom.Element.writexml
writexml = newwritexml

#local lib
from configServer import *

#ID3 tag library
import mutagen

#for md5 generation
import hashlib

def md5Checksum(filePath):
    fh = open(filePath, 'rb')
    m = hashlib.md5()
    while True:
        data = fh.read(8192)
        if not data:
            break
        m.update(data)
    return m.hexdigest()

indent=""
newl="\n"
encoding="UTF-8"

# Regular expression to find trailing spaces before a newline

def gen_xml_db(directory, tagKept = config.defaultTagKept, fileExt = config.defaultFileExt, dbLocation = config.defaultDbLocation, dbFile = config.defaultDbFile):
    """create xml database (location : dbLocation) with tag in tagKept, for the files in the directory with the extension in defaultFileExt"""
    if(directory == ""):
        log.error("create db: Bad directory given")
        return False
    
    doc = Document()
    root = doc.createElement("db")
    doc.appendChild(root)
    
    #classic loops to check every files in the subdirectories at every level. Possibly long.
    for dirname, dirnames, filenames in os.walk(directory):
        for f in filenames:
            if os.path.splitext(f)[1].lower() in fileExt:
                fileLocation = os.path.join(dirname, f) 
                block = doc.createElement("file")
                block.setAttribute("id", md5Checksum(fileLocation))
                root.appendChild(block)
                location = doc.createElement("location")
                location.setAttribute('value', fileLocation)
                block.appendChild(location)
                tag = dict()
                tagValue = dict()
                
                try:    
                    audio = mutagen.File(fileLocation, easy = True)
                    #for each tag given by mutagen, we add it to our library, useless to add unknow, load_db will do it alone.
                    for i in set(audio.keys()).intersection(tagKept):
                        tag[i] = doc.createElement(i)
                        tag[i].setAttribute('value', audio[i][0].encode("utf-8"))
                        block.appendChild(tag[i])
                except:
                    log.debug("create db: Bad file encoding : " + fileLocation)
    
    #writing the result into "db.xml" (defaultpath)
    try:
        db = open(dbLocation + dbFile, "w")
        doc.writexml(db, indent = indent, newl = newl)
        db.close()
    except:
        log.error("create db: Problem writing database")
        return False
    else:
        log.info("create db: Database created at " + dbLocation)
        return True



def update_xml_db(directory, lastUpdate = [0], tagKept = config.defaultTagKept, fileExt = config.defaultFileExt, dbLocation = config.defaultDbLocation, dbFile = config.defaultDbFile):
    """create xml database (location : dbLocation) with tag in tagKept, for the files in the directory with the extension in defaultFileExt"""
    if(directory == ""):
        log.error("update db: Bad directory given")
        return False
    
    log.debug("update db: Beginning to scan files")
 
    doc = minidom.parse(dbLocation + dbFile)
    
    #removing xml before creating the next
    try:
        os.remove(dbLocation + dbFile)
    except:
        log.debug("update db: cannot remove db file")
    #creating doc
    root = doc.documentElement
    
    #creating list of hashes
    nodes = root.getElementsByTagName('file')
    hashes = [e.getAttribute('id') for e in nodes]

    #classic loops to check every files in the subdirectories at every level. Possibly long.
    for dirname, dirnames, filenames in os.walk(directory):
        for f in filenames:
            fileLocation = os.path.join(dirname, f)
            md5 = md5Checksum(fileLocation)
#check if the file is not already in the xml
            if os.path.splitext(f)[1].lower() in fileExt and md5 not in hashes:
                block = doc.createElement("file")
                block.setAttribute("id", md5)
                root.appendChild(block)
                location = doc.createElement("location")
                location.setAttribute('value', fileLocation)
                block.appendChild(location)
                tag = dict()
                tagValue = dict()
                
                try:    
                    audio = mutagen.File(fileLocation, easy = True)
                    #for each tag given by mutagen, we add it to our library, useless to add unknow, load_db will do it alone.
                    for i in set(audio.keys()).intersection(tagKept):
                        tag[i] = doc.createElement(i)
                        tag[i].setAttribute('value', audio[i][0].encode("utf-8"))
                        block.appendChild(tag[i])
                except:
                    log.debug("update db: Bad file encoding : " + fileLocation)

    try:
        #Removes all TEXT_NODES in parameter nodes
        for node in root.childNodes:
            if node.nodeType == node.TEXT_NODE:
                node.data = ''
            else:
                for othernode in node.childNodes:
                    if othernode.nodeType == othernode.TEXT_NODE:
                        othernode.data = ''
    
        root.normalize()
    
        db = open(dbLocation + dbFile, "w")
        doc.writexml(db, indent = indent, newl = newl)
        db.close()
    except:
        log.error("update db: Problem writing during updating database")
        return False
    else:
        log.info("update db: Database updated at " + dbLocation)
        lastUpdate[0] = time()
        return True

def thread_update_db(directory):
    """Launch thread of updating db not to freeze other python script"""
    thread_that(update_xml_db, (directory,))

def thread_create_db(directory):
    """Launch thread of updating db not to freeze other python script"""
    thread_that(creat_xml_db, (directory,))

def thread_that(function, arguments):
    """Explicit name"""
    running = Thread(target = function, args = arguments)
    running.start()
