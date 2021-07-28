import os
import re
from pprint import pprint
from pathlib import Path
from datetime import datetime, timedelta

import slack
from dotenv import load_dotenv

from spotify_client import getPlaylist, isExistsTrackInPlaylist, addPlaylistTracks


env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

CHANNEL_ID = os.environ['CHANNEL_ID']
PLAYLIST_ID = os.environ['PLAYLIST_ID']
SLACK_TOKEN = os.environ['SLACK_TOKEN']

client = slack.WebClient(token=SLACK_TOKEN)


def getMessages(channel_id):
    try:
        messageList = dict()
        now = datetime.now()
        todayMorning = datetime(now.year, now.month, now.day, 0, 0, 0).timestamp()
        todayNight = datetime(now.year, now.month, now.day, 23, 59, 59).timestamp()
        msg = {
            'latest': todayNight,
            'oldest': todayMorning,
        }
        response = client.conversations_history(channel=channel_id,**msg).data

        for message in response['messages']:
            messageList[message['client_msg_id']] = {
                'user_id' : message['user'],
                'ts' : message['ts'],
                'text' : message['text']
            }
        return messageList
    except:
        return False


def checkMessageSpotifyUrl(messages):
    tracks = set()
    for msg in messages.values():
        txt = msg['text']
        regex = 'https:\/\/open.spotify.com\/track\/[a-zA-Z0-9]{1,256}'
        matches = re.findall(regex, txt)
        for url in matches:
            tracks.add(url)
    
    return list(tracks)


if __name__ == "__main__":

    messages = getMessages(CHANNEL_ID)
    if messages:
        track_list = checkMessageSpotifyUrl(messages)
        print(track_list)

        playlist = getPlaylist(PLAYLIST_ID)
        #pprint(playlist)

        tracks = list()
        for track in track_list:
            if not (isExistsTrackInPlaylist(playlist,track)):
                tracks.append(track)
        
        print(tracks)
        
        if tracks:
            addPlaylistTracks(PLAYLIST_ID, tracks)
