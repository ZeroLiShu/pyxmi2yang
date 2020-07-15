#!/usr/bin/python
import xml.dom.minidom

def parseModule(file):
    # build a dom tree
    DOMTree = xml.dom.minidom.parse(file)

    collection = DOMTree.documentElement

    print("collection ", collection)

def parseFiles(files):
    for file in files:
        parseModule(file)