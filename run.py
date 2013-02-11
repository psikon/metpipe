#!/usr/bin/env python

from bin.misc import helper
from bin.misc import switch
import ConfigParser

parameter = ConfigParser.ConfigParser()
parameter.read("parameter.txt")


program = parameter.get("Assembly","program")
print program

for case in switch(program):
    if case('abyss'):
        print "starte abyss"
        break
    if case('metaidba'):
        print "starte metaidba"
        break
    if case('metavelvet'):
        print "starte metavelvet"
        break
    if case('stitch'):
        print "starte stitch"
        break
    if case(): # default, could also just omit condition or 'if True'
        print "something else!"






