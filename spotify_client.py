import os
from pathlib import Path
from pprint import pprint

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth, CacheFileHandler
from dotenv import load_dotenv


env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
CLIENT_ID = os.environ['SPOTIFY_CLIENT_ID']
CLIENT_SECRET = os.environ['SPOTIFY_CLIENT_SECRET']
USER_NAME = os.environ['USER_NAME']

#sp = spotipy.Spotify(auth=os.environ['SPOTIFY_OAUTH'])
#sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))
SCOPE = 'playlist-modify-public,playlist-modify-private,playlist-read-private,' + \
        'playlist-read-collaborative,user-follow-modify,user-follow-read,' + \
        'user-library-modify,user-library-read,user-read-email,user-read-private,' + \
        'user-read-recently-played,user-top-read,user-read-playback-position'
try:
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                client_secret=CLIENT_SECRET,
                                                redirect_uri='http://localhost:9090',
                                                scope=SCOPE,
                                                cache_handler=CacheFileHandler(
                                                    cache_path=".cache-spotify",
                                                    username=USER_NAME
                                                )))
except:
    print('An error was encountered during authorization')
    exit(1)


def getPlaylist(playlist_id):
    playList = dict()
    try:
        resp = sp.playlist(playlist_id=playlist_id)
        while True:
            try:
                items = resp['tracks']['items']
            except:
                items = resp['items']

            for item in items:
                artistName = item['track']['artists'][0]['name']
                artistId = item['track']['artists'][0]['id']
                trackUrl = item['track']['external_urls']['spotify']
                trackId = item['track']['id']
                trackName = item['track']['name']

                playList[trackId] = {'track_name':trackName, 
                                    'track_url':trackUrl, 
                                    'artist_id':artistId, 
                                    'artist_name':artistName
                }
            
            try:
                nextURL = resp['tracks']['next']
                nextStation = resp['tracks']
            except:
                nextURL = resp['next']
                nextStation = resp

            if nextURL != None:
                resp = sp.next(nextStation)
            else:
                break
    except:
        print('Unexpected error while retrieving playlist data')
        
    return playList


def isExistsTrackInPlaylist(playlist,track_url):
    try:
        for key in playlist.values():
            if key['track_url'] == track_url:
                return True

        return False
    except:
        print('Unexpected error during TRACK check')
        return True


def addPlaylistTracks(playlist_id, trackList):
    try:
        sp.playlist_add_items(playlist_id=playlist_id, items=trackList)
        print('Add to Playlist Successful')
    except:
        print('Add to Playlist Unsuccessful')


if __name__ == '__main__':
    track_id = '18yBnbSt7VvEVV3Hkm9xwV'
    track_url = 'https://open.spotify.com/track/18yBnbSt7VvEVV3Hkm9xwV'
    playlist_id = '3kSZIBJTHozHljx6vC3ytA'
    
    playlist = getPlaylist(playlist_id)
    print(playlist)
    print(len(playlist))

    pprint(isExistsTrackInPlaylist(playlist,track_url))



    
