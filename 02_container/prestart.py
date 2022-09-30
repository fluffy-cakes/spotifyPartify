#!/usr/bin/env python3

import spotipy

scope         = 'user-read-currently-playing,user-modify-playback-state,user-read-playback-state'
cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path='./cached_token')
auth_manager  = spotipy.oauth2.SpotifyOAuth(
    cache_handler = cache_handler,
    open_browser  = False,
    redirect_uri  = 'http://127.0.0.1:80/',
    scope         = scope,
    show_dialog   = True
)

auth_url = auth_manager.get_authorize_url()
spotify  = spotipy.Spotify(auth_manager=auth_manager)
spotify.user('xx-xxx')
spotify.current_user_playing_track()

print("I AM DONE!")