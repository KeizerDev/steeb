#!/usr/bin/env python

import requests, sys, os, argparse, musicbrainzngs
from clint.textui import colored, puts, progress, indent
from mutagen.mp3 import EasyMP3

def get_album_metadata( url ):
    request = requests.get(url)

def download_file(url, path):
    r = requests.get(url, stream=url)
    with open(path, 'wb') as f:
        total_length = int(r.headers.get('content-length'))
        for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
    return path

def tag_file( filename, artist , title ):
    try:
        song = EasyMP3( filename )
        song["artist"] = artist
        song["title"] = title
        song.save()
    except Exception, e:
        print e

def download_tracks( album_data ):
    artist = album_data["artist"].replace(" ","_")
    album_name = album_data["current"]["title"].replace(" ","_")
    directory = artist + " - " + album_name
    directory = directory.replace("/"," - ")
    if not os.path.exists(directory):
        os.makedirs(directory)

    for track in album_data["trackinfo"]:
        print colored.cyan("Downloading %s by %s." % ( track["title"] ,artist ) )
        track_name = track["title"].replace(" ","_")
        track_number = str(track["track_num"]).zfill(2)
        track_filename=  '%s_%s.mp3' %( track_number ,track_name);
        path = directory + "/" + track_filename
        download_file( track["file"]["mp3-128"] , path)
        tag_file( path , artist , track["title"])


def get_albums( artist_id ):
    result = musicbrainzngs.get_artist_by_id(artist_id, includes=["release-groups"], release_type=["album", "ep"])
    
    for idx, album in enumerate(result["artist"]["release-group-list"]):
        with indent(4, quote=''):
            puts("[{0}]. {1}".format(colored.yellow((idx + 1)), album["title"]))
            # puts("%s" % (idx + 1))
            # puts("%s" % album["title"])


def search_artist( search_query ):
    result = musicbrainzngs.search_artists(artist=search_query)
    print("steeb found %s artists" % colored.cyan(len(result["artist-list"])))
    for idx, artist in enumerate(result["artist-list"]):
        with indent(4, quote=''):
            puts("[{0}]. {1}".format(colored.yellow((idx + 1)), artist["name"]))
            # get_albums(artist["id"])


def main():
    musicbrainzngs.set_useragent("steeb", "0.1", "KeizerDev@github.com")

    parser = argparse.ArgumentParser(description="Steeb. A reverse way of beets by downloading music from pleer.com\n")
    parser.add_argument("artist_query", metavar="artist", type=str, help="Artist search query")

    vargs = vars(parser.parse_args())
    if not any(vargs.values()):
        parser.error("Please supply a band albums url.")
    search_artist( vargs["artist_query"] )

if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception, e:
        print e

