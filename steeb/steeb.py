#! /usr/bin/env python

import demjson, requests, sys, os, argparse
from clint.textui import colored, puts, progress
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

def main():
    parser = argparse.ArgumentParser(description='BcampScrape. Scrape and download an artist album from BandCamp.\n')
    parser.add_argument('album_url', metavar='U', type=str,help="A BandCamp band album url")
    args = parser.parse_args()
    vargs = vars(args)
    if not any(vargs.values()):
        parser.error("Please supply a band albums url.")
    album_data = get_album_metadata( vargs["album_url"] )
    download_tracks( album_data )


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception, e:
        print e

