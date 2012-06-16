#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

#adding path of audio player to the lib
import sys

if 'client/' not in sys.path:
    sys.path.append('client/')

#running client 
import client 
