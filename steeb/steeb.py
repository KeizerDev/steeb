#!/usr/bin/env python
# -*- coding: utf8 -*-

from __future__ import with_statement   # for python 2.5 compatibility

__author__ = "KeizerDev (robertjankeizer@gmail.com)"
__copyright__ = "Copyright (C) 2015- KeizerDev"
__license__ = "LGPL 3.0"

import requests, sys, os, argparse, time, urllib2
import preference as pref
import musicbrainzngs as m
import helpers.pleer as pleer
from Tkinter import *
from clint.textui import colored, puts, progress, indent

# --- here goes your event handlers ---
def search_artist(evt):
    result = m.search_artists(artist=mainwin['searchfield'].value)
    resultList = []
    print("steeb found %s artists" % colored.cyan(len(result["artist-list"])))
    for idx, artist in enumerate(result["artist-list"]):
        resultList.append([artist["name"], artist["id"]])

    lv = mainwin['artistslist']
    lv.items = resultList


def get_albums(evt):
    result = m.get_artist_by_id(evt.target.get_selected_items()[0]['id'], includes=["release-groups"], release_type=["album", "ep"])
    resultList = []
    print(result)
    for idx, album in enumerate(result["artist"]["release-group-list"]):
        resultList.append([album["title"], album["id"]])

    lv = mainwin['albumslist']
    lv.items = resultList


def get_tracks(evt):
    albumslist = m.get_release_group_by_id(evt.target.get_selected_items()[0]['id'], includes="releases")
    resultList = []

    print("=========================")
    print("=========================")
    print(albumslist)
    print("=========================")
    print("=========================")
    tracks = m.get_release_by_id(albumslist['release-group']['release-list'][0]['id'], includes=["artists", "recordings"])

    album_id = tracks["release"]["id"]
    for idx, track in enumerate(tracks["release"]["medium-list"][0]["track-list"]):
        resultList.append([track["recording"]["title"], album_id])

    lv = mainwin['trackslist']
    lv.items = resultList


def clickevt_album(evt):
    window_name = mainwin['artistslist'].get_selected_items()[0]["artist"] + " - " + mainwin['albumslist'].get_selected_items()[0]["albums"];

    with gui.Window(name='downwin', title=u'' + window_name, height=down_win_height, width=down_win_width, left='323', top='137', bgcolor=u'#F0F0F0', fgcolor=u'#555555', ):
        gui.TextBox(name='downloadpath', value=pref.download_dir, height=form_height, left='5', top='0', width=down_input_width, parent='downwin', )
        gui.Button(label=u'Download all!', name='btn_down_all', height='35px', width=down_btn_width, left=down_input_width, top='5', default=True, fgcolor=u'#EEEEEE', bgcolor=u'#C0392B', parent='downwin', )
        gui.Button(label=u'Download selected!', name='button_down', height='35px', width=down_btn_width, left=down_btn_left, top='5', default=True, fgcolor=u'#EEEEEE', bgcolor=u'#C0392B', parent='downwin', )
        with gui.ListView(name='downloadlist', height=down_lv_songs_height, width=down_win_width, left='0', top=form_height, item_count=10, sort_column=0, onitemselected="print ('sel %s' % event.target.get_selected_items())", ):
            gui.ListColumn(name='trackposition', text='Nr.', width=50)
            gui.ListColumn(name='tracks', text='Tracks', width=300)
            gui.ListColumn(name='tracksfound', text='Tracks found', width=150)
            gui.ListColumn(name='id', text='', width=0)
        gui.Gauge(name='progressbar', height=down_gauge_height, left=0, top=down_gauge_top, width=down_win_width, value=0, )

    downwin = gui.get("downwin")
    downwin['btn_down_all'].onclick = download_all_songs
    plr = pleer.Pleer()
    # print(pleer.Pleer())


    tracksList = []
    (oldtracks_position, oldtracks_json) = mainwin["trackslist"].items()[0]

    tracks = m.get_release_by_id(oldtracks_json["id"], includes=["artists", "recordings"])
    print(tracks)
    for idx, track in enumerate(tracks["release"]["medium-list"][0]["track-list"]):
        print(idx)

        tracksList.append(plr.search(mainwin['artistslist'].get_selected_items()[0]["artist"] + " " + track["recording"]["title"], track))

    lv = downwin["downloadlist"]
    lv.items = tracksList


def download_all_songs(self):
    downwin = gui.get("downwin")
    for track in downwin["downloadlist"].items:
        if (track["id"] != ""):
            song_url = "http://pleer.com/browser-extension/files/%s.mp3" % track["id"]
            song_title = "%s - %s" % (mainwin['artistslist'].get_selected_items()[0]["artist"], track["tracks"])
            download(downwin, song_url, song_title)

def download(downwin, fileurl, file_name):
    downwin['progressbar'].value = 30

    u = urllib2.urlopen(fileurl)
    if not os.path.exists(pref.download_dir):
        os.makedirs(pref.download_dir)

    if not os.path.exists(pref.download_dir + "/" + file_name + ".mp3"):

        f = open(os.path.join(pref.download_dir, file_name + ".mp3"), 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])

        print "Downloading: %s Bytes: %s" % (file_name, file_size)

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)
            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            downwin['progressbar'].value = int(round(file_size_dl * 100. / file_size))
            # downwin["progressbar"].value = int(round(file_size_dl * 100. / file_size))
            status = status + chr(8)*(len(status)+1)
            print status,

        f.close()
    else:
        print ("File " + file_name + " already downloaded")

def load(evt):
    m.set_useragent("steeb", "0.1", "KeizerDev@github.com")
    mainwin['button_search'].onclick = search_artist
    mainwin['artistslist'].onitemselected = get_albums
    mainwin['albumslist'].onitemselected = get_tracks
    mainwin['button_down'].onclick = clickevt_album
    lv = mainwin['artistslist']

# Layout styles
#downwin
down_win_height = '400px'
down_win_width = '500px'

down_input_width = '260px'
down_btn_width = '120px'
down_btn_left = '380px'

down_lv_songs_height = '335px'
down_gauge_top = '380px'
down_gauge_height = '20px'

#mainwin
main_win_height = '500px'
main_win_width = '600px'

main_search_width = '400px'
main_songs_width = '200px'
main_input_width = '320px'
main_btn_width = '60px'

lv_artist_height = '235px'
lv_albums_height = '220px'
lv_songs_height = '455px'
lv_artist_top = '280px'

#global
btn_download_width = '100px'
form_height = '45px'

root = Tk()

root.geometry("500x600")
root.resizable(width=FALSE, height=FALSE)
for r in range(3):
    for c in range(5):
        Label(root, text='R%s/C%s'%(r,c),borderwidth=1 ).grid(row=r,column=c)

# with gui.Window(name='mainwin', title=u'Steeb', height=main_win_height, width=main_win_width, left='323', top='137', bgcolor=u'#F0F0F0', fgcolor=u'#555555', image='', ):
#     gui.TextBox(name='searchfield', height=form_height, left='5', top='0', width=main_input_width, parent='mainwin', )
#     gui.Button(label=u'Crawl songs!', name='button_down', height='35px', width=btn_download_width, left=main_search_width, top='5', default=True, fgcolor=u'#EEEEEE', bgcolor=u'#C0392B', parent='mainwin', )
#     gui.Button(label=u'Search!', name='button_search', height='35px', width=main_btn_width, left='333px', top='5', default=True, fgcolor=u'#EEEEEE', bgcolor=u'#C0392B', parent='mainwin', )
#     with gui.ListView(name='artistslist', height=lv_artist_height, left='0', top=form_height, width=main_search_width, item_count=10, sort_column=0, onitemselected="print ('sel %s' % event.target.get_selected_items())", ):
#         gui.ListColumn(name='artist', text='Artist', width=400)
#         gui.ListColumn(name='id', text='Id', width=0)
#     with gui.ListView(name='albumslist', height=lv_albums_height, left='0', top=lv_artist_top, width=main_search_width, item_count=10, sort_column=0, onitemselected="print ('sel %s' % event.target.get_selected_items())", ):
#         gui.ListColumn(name='albums', text='Albums', width=400)
#         gui.ListColumn(name='id', text='Id', width=0)
#     with gui.ListView(name='trackslist', height=lv_songs_height, left=main_search_width, top=form_height, width=main_songs_width, item_count=10, sort_column=0, onitemselected="print ('sel %s' % event.target.get_selected_items())", ):
#         gui.ListColumn(name='songs', text='Songs', width=200)
#         gui.ListColumn(name='id', text='Id', width=0, )
#         # gui.Gauge(name='gauge', height='18', left='13', top='130', width='50', value=50, )
    # Code to add widgets will go here...


# mainwin = gui.get("mainwin")

# mainwin.onload = load

if __name__ == "__main__":
    root.mainloop()