from app.lib.singleton import Singleton
import requests
import base64
import datetime

class SpotifyClient(metaclass=Singleton):
  config = None
  token = None

  def __init__(self, config):
    self.config = config

  def refresh_token(self):
    headers = self._build_refresh_headers()
    data = {'grant_type': 'refresh_token', 'refresh_token': self.config.spotify_refresh_token}
    request = requests.post('https://accounts.spotify.com/api/token', data = data, headers = headers)
    response = request.json()
    self.config.insert_into_storage('spotify_access_token', response['access_token'])
    token_expiration = datetime.datetime.now() + datetime.timedelta(seconds=response['expires_in'])
    self.config.insert_into_storage('spotify_expires_at', token_expiration)
    return response

  def fetch_current_song(self):
    return self._send_get_request('https://api.spotify.com/v1/me/player/currently-playing')

  def fetch_song_analysis(self, id):
    return self._send_get_request('https://api.spotify.com/v1/audio-analysis/' + id)

  def _build_headers(self):
    return { 'Authorization': 'Bearer ' + self.config.spotify_access_token }

  def _build_refresh_headers(self):
    auth_header = self.config.spotify_client_id + ':' + self.config.spotify_client_secret
    auth_header = base64.b64encode(auth_header.encode('ascii')).decode('ascii')
    auth_header = 'Basic ' + auth_header
    return {'Authorization': auth_header, 'Content-Type': 'application/x-www-form-urlencoded'}

  def _send_get_request(self, url):
    if (self.config.is_token_expired()):
      self.refresh_token()
    headers = self._build_headers()
    request = requests.get(url, headers = headers)
    response = request.json()
    return response