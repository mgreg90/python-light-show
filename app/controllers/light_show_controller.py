from app.lib.spotify_client import SpotifyClient
import json
import datetime
import pdb

def create():
  song = SpotifyClient().fetch_current_song()
  songId = song['item']['id']
  songAnalysis = SpotifyClient().fetch_song_analysis(songId)

  start_time = datetime.datetime.now()
  song_progress_ms = datetime.timedelta(milliseconds=song['progress_ms'])
  song_duration_ms = datetime.timedelta(milliseconds=song['item']['duration_ms'])
  offset = datetime.timedelta(milliseconds=0)

  beats = songAnalysis['beats']

  next_beat_index = _find_first_future_beat(beats, song_progress_ms)
  n = 0
  while song_progress_ms + offset < song_duration_ms:
    next_beat_start = datetime.timedelta(seconds=beats[next_beat_index]['start'])

    if (song_progress_ms + offset > next_beat_start):
      print('flash lights!!!' + str(n))
      beats = beats[(next_beat_index + 1):]
      next_beat_index = _find_first_future_beat(beats, song_progress_ms + offset)
      n += 1
    
    offset = datetime.datetime.now() - start_time
  return {
    'status': 'running'
  }

def _find_first_future_beat(beats, progress_ms):
  for beat_idx in range(len(beats)):
    beat_start = datetime.timedelta(seconds=beats[beat_idx]['start'])
    beat_confidence = beats[beat_idx]['confidence']
    if (beat_start > progress_ms and beat_confidence > 0.1):
      return beat_idx