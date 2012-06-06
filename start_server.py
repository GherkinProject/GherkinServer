#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

#adding path of audio player to the lib
import sys
from configServer import *

if config.root + 'server/' not in sys.path:
    sys.path.append(config.root + 'server/')

if config.root + 'db-tools/' not in sys.path:
    sys.path.append(config.root + 'db-tools/')


#running server
import ai
