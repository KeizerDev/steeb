# -*- coding: utf8 -*-

import requests

class Pleer:
    
    def search(self, keywords, track):
        pleer_qry = requests.get("http://pleer.com/browser-extension/search?q=%s" % keywords)
        pleer_tracks = pleer_qry.json()['tracks']

        print(pleer_tracks)
        if len(pleer_tracks) > 0:
            # Create something like a magically selection algorithm
            return [track["number"], track["recording"]["title"], "✓".decode('utf-8'), pleer_tracks[0]["id"]]
        else:
            # TODO: Do another search for the track
            return [track["number"], track["recording"]["title"], "×".decode('utf-8'), ""]
        