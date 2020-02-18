import os
import yaml
import datetime
from app.lib.singleton import Singleton

class Config(metaclass=Singleton):
  _storage = None

  def __init__(self):
    self.spotify_client_id = os.getenv('SPOTIFY_CLIENT_ID')
    self.spotify_client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    self.spotify_authorization_code = os.getenv('SPOTIFY_AUTHORIZATION_CODE')
    self.spotify_access_token = self.fetch_from_storage('spotify_access_token')
    self.spotify_refresh_token = self.fetch_from_storage('spotify_refresh_token')
    self.spotify_token_expires_at = self.fetch_from_storage('spotify_expires_at')

  def fetch_from_storage(self, key):
    if (self._storage is not None):
      return self._storage[key]

    with open(self._storage_file()) as file:
      self._storage = yaml.load(file, Loader=yaml.FullLoader)
    return self._storage[key]

  def insert_into_storage(self, key, value):
    self._storage[key] = value
    with open(self._storage_file(), 'w') as file:
      yaml.dump(self._storage, file)
  
  def is_token_expired(self):
    return not self.spotify_token_expires_at or datetime.datetime.now() >= self.spotify_token_expires_at

  def _storage_file(self):
    this_dir = os.path.dirname(__file__)
    return os.path.join(this_dir, '../data/spotify.yaml')
