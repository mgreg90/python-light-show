import os
from app import create_app, register_routes
from app.lib import Config, SpotifyClient
from dotenv import load_dotenv

APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

application = create_app()
register_routes(application)

config = Config()
spotify_client = SpotifyClient(config)