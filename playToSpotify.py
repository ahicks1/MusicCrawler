import sys
from gmusicapi import Mobileclient
import spotipy
import spotipy.util as util
import pickle
import re


class Song:
    def __init__(self,name,artist):
        self.name = name
        self.artist = artist
        self.id = ""

class Playlist:

    def __init__(self,songs=[],id=""):
        self.id = id
        self.name = raw_input('What is the name of the playlist? ')
        self.songs = songs

    def pushToSpotify(self):
        spCred = util.prompt_for_user_token("legofan0329",'playlist-modify-private',client_id='c672bcf1f58c4627ad825af8cfa00ef7',client_secret='2192308c9b104ec586e2194b2f838fde',redirect_uri='http://localhost/')
        spotify = spotipy.Spotify(auth=spCred)
        playlist = spotify.user_playlist_create("legofan0329",self.name,False)
        ids = []
        for song in self.songs:
            res = spotify.search(song.name+" "+song.artist,1,0,'track')
            if( len(res['tracks']['items']) > 0):
                ids.append(res['tracks']['items'][0]['id'])
            else:
                print("Didn't find "+song.name)
        chunks = [ids[x:x+100] for x in xrange(0, len(ids), 100)]
        for chunk in chunks:
            spotify.user_playlist_add_tracks("legofan0329",playlist['id'],chunk)



    def fetchFromGooglePlay(self,pc):
        playlists = pc.get_all_user_playlist_contents()
        for playlist in playlists:
            pname = playlist["name"]
            if(pname == self.name):
                for song in playlist["tracks"]:
                    try:
                        sn = Song(re.sub('\((.+)\)', '',song['track']['title']),song['track']['artist'])
                        #print sn.name
                        self.songs.append(sn)
                    except KeyError:
                        print "song failed info"

    def fetchFromFile(self):
        file = open("./"+self.name+".txt",'r')
        obj = pickle.load(file)
        print obj
        self.songs = obj.songs
        file.close()


    def outToFile(self):
        file = open("./"+self.name+".txt",'w+')
        pickle.dump(self,file)
        file.close()


def dictToSong(dict):
    return Song(dict)


if(len(sys.argv) < 1):
    print "please enter the name of the playlist"
    exit()

googlePlay = Mobileclient()
logged_in = googlePlay.login('legofan0329@gmail.com', '1944_D-d@y',Mobileclient.FROM_MAC_ADDRESS)
if(not logged_in):
    print "failed to login to google play"
    exit()
print "Choose a playlist: "
playlists = googlePlay.get_all_playlists()
for playlist in playlists:
    print playlist["name"]

list = Playlist()
list.fetchFromGooglePlay(googlePlay)
list.pushToSpotify()
#for song in list.songs:
    #print song.name
#list.fetchFromGooglePlay(googlePlay)
list.outToFile()
#list.pushToSpotify()
