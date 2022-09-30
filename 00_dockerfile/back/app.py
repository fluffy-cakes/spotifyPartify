#!/usr/bin/env python3

from time import sleep
import datetime
import flask
import json
import os
import random
import spotipy
import threading



writeToken = open("cached_token", "w")
writeToken.write(os.environ.get('CACHED_TOKEN'))
writeToken.close()



scope         = 'user-read-currently-playing,user-modify-playback-state,user-read-playback-state'
cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path='./cached_token')
auth_manager  = spotipy.oauth2.SpotifyOAuth(
    cache_handler = cache_handler,
    open_browser  = False,
    redirect_uri  = 'http://asdf.local/',
    scope         = scope,
    show_dialog   = True
)


auth_url = auth_manager.get_authorize_url()
spotify  = spotipy.Spotify(auth_manager=auth_manager)
spotify.current_user_playing_track()


apiCall      = ""
voteLimit    = 5
voteTime     = 45
voteMetaData = {
    "adminOverride"          : "false",
    "calcTimePercent"        : 0,
    "calcTimePlayed"         : "",
    "currentArtists"         : "ASDF",
    "currentImage"           : "",
    "currentTrack"           : "QWER",
    "currentTrackId"         : "",
    "currentUrl"             : "",
    "currentVoteDown"        : 0,
    "currentVoteLimit"       : voteLimit,
    "currentVoteSession"     : "CLOSED",
    "currentVoteTimerPercent": 0,
    "currentVoteTime"        : voteTime,
    "currentVoteTimer"       : 0,
    "currentVoteUp"          : 0
}


wifeOverride = [
    "0gusqTJKxtU1UTmNRMHZcv", # Dizzee
    "0Dc2rdPzleezxhvQhQbXuS", # Idris
    "0H39MdGGX6dbnnQPt6NQkZ", # SAINt JHN
    "2SrSdSvpminqmStGELCSNd"  # Stormzy
]



def currentSong():
    global apiCall, scope, wifeOverride, voteMetaData, voteTime
    def currentThread():
        global apiCall, scope, wifeOverride, voteMetaData, voteTime

        randomInt = random.randint(1, 100)

        while True:
            print("RANDOM: {}".format(randomInt))
            cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path='./cached_token')
            auth_manager  = spotipy.oauth2.SpotifyOAuth(
                cache_handler = cache_handler,
                redirect_uri  = 'http://127.0.0.1:5000/',
                scope         = scope,
                show_dialog   = True
            )
            sp      = spotipy.Spotify(auth_manager=auth_manager)
            apiCall = sp.current_user_playing_track()

            while apiCall is None or apiCall['is_playing'] == False:
                voteMetaData = {
                    "adminOverride"          : "false",
                    "calcTimePercent"        : 0,
                    "calcTimePlayed"         : "",
                    "currentArtists"         : "ASDF",
                    "currentImage"           : "",
                    "currentTrack"           : "Qwerty",
                    "currentTrackId"         : "",
                    "currentUrl"             : "",
                    "currentVoteDown"        : 0,
                    "currentVoteLimit"       : voteLimit,
                    "currentVoteSession"     : "CLOSED",
                    "currentVoteTime"        : voteTime,
                    "currentVoteTimer"       : 0,
                    "currentVoteTimerPercent": 0,
                    "currentVoteUp"          : 0
                }
                print("\n\nI SLEEPS NOW\n\n")
                sleep(2)
                apiCall = sp.current_user_playing_track()

            allArtists = []
            for artist in apiCall['item']['artists']:
                allArtists.append(artist['name'])

            allArtistsIds = []
            for artist in apiCall['item']['artists']:
                allArtistsIds.append(artist['id'])

            voteMetaData['currentArtists'] = ', '.join(allArtists)
            voteMetaData['currentImage']   = apiCall['item']['album']['images'][1]['url']
            voteMetaData['currentTrack']   = apiCall['item']['name']
            voteMetaData['currentUrl']     = apiCall['item']['external_urls']['spotify']

            if voteMetaData['currentTrackId'] != apiCall['item']['id']:
                voteMetaData['currentTrackId']     = apiCall['item']['id']
                voteMetaData['adminOverride']      = "false"
                voteMetaData['currentVoteDown']    = 0
                voteMetaData['currentVoteUp']      = 0
                voteMetaData['currentVoteSession'] = "WIFE OVERRIDE!"

            millis  = apiCall['progress_ms']
            millis  = int(millis)
            seconds = (millis/1000)%60
            seconds = int(seconds)
            minutes = (millis/(1000*60))%60
            minutes = int(minutes)

            voteMetaData["calcTimePlayed"]  = "{} min {}sec".format(minutes, seconds)
            voteMetaData["calcTimePercent"] = int(int(apiCall['progress_ms']) / int(apiCall['item']['duration_ms']) * 100)

            calcTime = (voteTime * 1000)

            if apiCall['progress_ms'] < calcTime:
                countDown                               = int((calcTime - apiCall['progress_ms'])/1000)
                voteMetaData['currentVoteTimer']        = countDown
                voteMetaData['currentVoteTimerPercent'] = int(countDown / voteTime * 100)

                if voteMetaData['currentVoteUp'] < voteMetaData['currentVoteLimit']:
                    for i in allArtistsIds:
                        if i in wifeOverride:
                            voteMetaData['currentVoteSession'] = "WIFE OVERRIDE!"
                            print("\n{}\n{}\n".format(datetime.datetime.now(), voteMetaData))
                            break
                        else:
                            if voteMetaData['adminOverride'] == "true":
                                voteMetaData['currentVoteSession'] = "WIFE OVERRIDE!"
                                print("\n{}\n{}\n".format(datetime.datetime.now(), voteMetaData))
                            else:
                                voteMetaData['currentVoteSession'] = "OPEN"
                                print("\n{}\n{}\n".format(datetime.datetime.now(), voteMetaData))
                else:
                    voteMetaData['currentVoteSession'] = "CLOSED"
                    print("\n{}\n{}\n".format(datetime.datetime.now(), voteMetaData))
                sleep(2)
            else:
                voteMetaData['currentVoteTimer']   = 0
                voteMetaData['currentVoteSession'] = "CLOSED"
                print("\n{}\n{}\n".format(datetime.datetime.now(), voteMetaData))
                sleep(2)
    thread = threading.Thread(target=currentThread)
    thread.start()



def objectMaker():
    global voteMetaData
    print("\n{}\nOBJECTMAKER: {}\n".format(datetime.datetime.now(), voteMetaData))
    return voteMetaData



def nextSong():
    global scope, voteMetaData
    deviceId = ''

    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path='./cached_token')
    auth_manager  = spotipy.oauth2.SpotifyOAuth(
        cache_handler = cache_handler,
        redirect_uri  = 'http://127.0.0.1:5000/',
        scope         = scope,
        show_dialog   = True
    )
    sp      = spotipy.Spotify(auth_manager=auth_manager)
    apiCall = sp.devices()
    print(apiCall)
    for device in apiCall['devices']:
        if device['is_active'] == True:
            deviceId = device['id']
            print(device['name'])
    sp.next_track(device_id=deviceId)
    voteMetaData['currentVoteSession'] = "OPEN"
    voteMetaData['currentVoteDown']    = 0
    voteMetaData['currentVoteUp']      = 0


currentSong()



# FLASK
app = flask.Flask(__name__)



@app.route('/', methods=['GET'])
def getUI():
    return json.dumps(objectMaker())



@app.route('/api/downvote', methods=['POST'])
def downvote():
    global voteMetaData
    print("\n\nDOWN\n\n")
    if voteMetaData['currentVoteSession'] == "OPEN":
        if (voteMetaData['currentVoteDown'] < voteMetaData['currentVoteLimit'] and
            voteMetaData['currentVoteUp']   < voteMetaData['currentVoteLimit']):
            voteMetaData['currentVoteDown'] += 1
            if voteMetaData['currentVoteDown'] >= voteMetaData['currentVoteLimit']:
                print("NEXT!")
                sleep(2)
                nextSong()
        elif voteMetaData['currentVoteUp'] <= voteMetaData['currentVoteLimit']:
            voteMetaData['currentVoteDown'] += 1
    return json.dumps(True)



@app.route('/api/upvote', methods=['POST'])
def upvote():
    global voteMetaData
    print("\n\nUP\n\n")
    if voteMetaData['currentVoteSession'] == "OPEN":
        if voteMetaData['currentVoteUp'] <= voteMetaData['currentVoteLimit']:
            voteMetaData['currentVoteUp'] += 1
    return json.dumps(True)



# ADMIN API
@app.route('/admin/limit/<count>', methods=['POST'])
def votelimit(count):
    global voteLimit, voteMetaData
    print("\n\nVOTE LIMIT NOW: {}\n\n".format(count))
    voteLimit                        = int(count)
    voteMetaData["currentVoteLimit"] = int(count)
    return json.dumps(True)



@app.route('/admin/time/<count>', methods=['POST'])
def votetime(count):
    global voteTime, voteMetaData
    print("\n\nVOTE TIMER NOW: {}\n\n".format(count))
    voteTime                        = int(count)
    voteMetaData["currentVoteTime"] = int(count)
    return json.dumps(True)



@app.route('/admin/over', methods=['GET'])
def override():
    global voteMetaData
    print("\n\nADMIN OVERRIDE\n\n")
    voteMetaData["adminOverride"] = "true"
    return json.dumps(True)



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)