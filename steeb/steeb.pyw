#!/usr/bin/env python

from __future__ import with_statement   # for python 2.5 compatibility

__author__ = "Robert-Jan Keizer (robertjankeizer@gmail.com)"
__copyright__ = "Copyright (C) 2013- Robert-Jan Keizer"
__license__ = "LGPL 3.0"

import gui, requests, sys, os, argparse, time
import musicbrainzngs as m
from clint.textui import colored, puts, progress, indent
from mutagen.mp3 import EasyMP3



m.set_useragent("steeb", "0.1", "KeizerDev@github.com")

# --- here goes your event handlers ---
def get_tracks(evt):
    albumslist = m.get_release_group_by_id(evt.target.get_selected_items()[0]['id'], includes="releases")
    resultList = [] 

    print("=========================")
    print("=========================")
    print(albumslist)
    print("=========================")
    print("=========================")
    print(albumslist['release-group']['release-list'][-1]['id'])
    tracks = m.get_release_by_id(albumslist['release-group']['release-list'][0]['id'], includes=["artists", "recordings"])
    print(tracks)
    for idx, track in enumerate(tracks["release"]["medium-list"][0]["track-list"]):
        resultList.append([track["recording"]["title"], track["id"]])

    lv = mywin['trackslist']
    lv.items = resultList



def get_albums(evt):
    result = m.get_artist_by_id(evt.target.get_selected_items()[0]['id'], includes=["release-groups"], release_type=["album", "ep"])
    resultList = []
    print(result)
    for idx, album in enumerate(result["artist"]["release-group-list"]):
        resultList.append([album["title"], album["id"]])
    lv = mywin['albumslist']
    lv.items = resultList

def search_artist(evt):
    result = m.search_artists(artist=mywin['searchfield'].value)
    resultList = []
    print("steeb found %s artists" % colored.cyan(len(result["artist-list"])))
    for idx, artist in enumerate(result["artist-list"]):
        resultList.append([artist["name"], artist["id"]])

    lv = mywin['artistslist']
    lv.items = resultList


def load(evt):
    lv = mywin['artistslist']

# Layout styles
win_height = '500px'
win_width = '600px'

search_width = '400px'
songs_width = '200px'
input_width = '320px'
btn_width = '60px'
btn_download_width = '100px'

form_height = '45px'
lv_artist_height = '235px'
lv_albums_height = '220px'
lv_songs_height = '455px'
lv_artist_top = '280px'


with gui.Window(name='mywin', title=u'Steeb', height=win_height, width=win_width, left='323', top='137', bgcolor=u'#F0F0F0', fgcolor=u'#555555', image='', ):
    gui.TextBox(name='searchfield', height=form_height, left='5', top='0', width=input_width, parent='mywin', )
    gui.Button(label=u'Download!', name='button', height='35px', width=btn_download_width, left=search_width, top='5', default=True, fgcolor=u'#F9F9F9', parent='mywin', )
    gui.Button(label=u'Search!', name='button', height='35px', width=btn_width, left='333px', top='5', default=True, fgcolor=u'#F9F9F9', parent='mywin', )
    with gui.ListView(name='artistslist', height=lv_artist_height, left='0', top=form_height, width=search_width, item_count=10, sort_column=0, onitemselected="print ('sel %s' % event.target.get_selected_items())", ):
        gui.ListColumn(name='artist', text='Artist', width=400)
        gui.ListColumn(name='id', text='Id', width=0)
    with gui.ListView(name='albumslist', height=lv_albums_height, left='0', top=lv_artist_top, width=search_width, item_count=10, sort_column=0, onitemselected="print ('sel %s' % event.target.get_selected_items())", ):
        gui.ListColumn(name='albums', text='Albums', width=400)
        gui.ListColumn(name='id', text='Id', width=0)
    with gui.ListView(name='trackslist', height=lv_songs_height, left=search_width, top=form_height, width=songs_width, item_count=10, sort_column=0, onitemselected="print ('sel %s' % event.target.get_selected_items())", ):
        gui.ListColumn(name='songs', text='Songs', width=200)
        gui.ListColumn(name='id', text='Id', width=0)

   
mywin = gui.get("mywin")

mywin.onload = load
mywin['button'].onclick = search_artist
mywin['artistslist'].onitemselected = get_albums
mywin['albumslist'].onitemselected = get_tracks

if __name__ == "__main__":
    mywin.show()    
    gui.main_loop()
