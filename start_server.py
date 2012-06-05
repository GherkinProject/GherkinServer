#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

#adding path of audio player to the lib
import sys
if 'server/' not in sys.path:
    sys.path.append('server/')

if 'db-tools/' not in sys.path:
    sys.path.append('db-tools/')


#running server
import ai
