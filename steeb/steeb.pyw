#!/usr/bin/env python

from __future__ import with_statement   # for python 2.5 compatibility

__author__ = "Robert-Jan Keizer (robertjankeizer@gmail.com)"
__copyright__ = "Copyright (C) 2013- Robert-Jan Keizer"
__license__ = "LGPL 3.0"

import gui, requests, sys, os, argparse, musicbrainzngs, time
from clint.textui import colored, puts, progress, indent
from mutagen.mp3 import EasyMP3



musicbrainzngs.set_useragent("steeb", "0.1", "KeizerDev@github.com")

# --- here goes your event handlers ---
def get_albums( artist_id ):
    result = musicbrainzngs.get_artist_by_id(artist_id, includes=["release-groups"], release_type=["album", "ep"])
    
    for idx, album in enumerate(result["artist"]["release-group-list"]):
        with indent(4, quote=''):
            puts("[{0}]. {1}".format(colored.yellow((idx + 1)), album["title"]))
            # puts("%s" % (idx + 1))
            # puts("%s" % album["title"])


def search_artist(evt):
    result = musicbrainzngs.search_artists(artist=mywin['searchfield'].value)
    resultList = []
    print("steeb found %s artists" % colored.cyan(len(result["artist-list"])))
    for idx, artist in enumerate(result["artist-list"]):
        with indent(4, quote=''):
            resultList.append(artist["name"])
            # lv.items = 
            # get_albums(artist["id"])
    lv = mywin['resultslist']
    lv.items = resultList


def load(evt):
    lv = mywin['resultslist']

# Layout styles
win_height = '500px'
win_width = '400px'
input_width = '320px'
btn_width = '60px'

form_height = '45px'
lv_height = '455px'

with gui.Window(name='mywin', title=u'Steeb', height=win_height, width=win_width, left='323', top='137', bgcolor=u'#F0F0F0', fgcolor=u'#555555', image='', ):
    gui.TextBox(name='searchfield', height=form_height, left='5', top='0', width=input_width, )
    gui.Button(label=u'Search!', name='button', height='35px', width=btn_width, left='333px', top='5', default=True, fgcolor=u'#F9F9F9', )
    with gui.ListView(name='resultslist', height=lv_height, left='0', top=form_height, width=win_width, item_count=10, sort_column=0, onitemselected="print ('sel %s' % event.target.get_selected_items())", ):
        gui.ListColumn(name='artist', text='Artist', width=400)


   
mywin = gui.get("mywin")

mywin.onload = load
mywin['button'].onclick = search_artist


if __name__ == "__main__":
    mywin.show()    
    gui.main_loop()
