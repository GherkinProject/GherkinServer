#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

#adding path of audio player to the lib
import sys
from configServer import *

#working on the database here
if config.root + 'db-tools/' not in sys.path:
    sys.path.append(config.root + 'db-tools/')

#running server
import create_db

#try:
create_db.update_xml_db(sys.argv[1])
#except:
#    print "absolute path for library needed"
