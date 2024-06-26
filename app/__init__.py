import os
from dotenv import load_dotenv

from .zoom_manager import ZoomClient, ZoomApp
from .transcriber import Transcriber

load_dotenv()

ZOOM_ACCOUNT_ID = os.environ.get("ZOOM_ACCOUNT_ID")
ZOOM_CLIENT_ID = os.environ.get("ZOOM_CLIENT_ID")
ZOOM_CLIENT_SECRET = os.environ.get("ZOOM_CLIENT_SECRET")


transcriber = Transcriber()

client = ZoomClient(account_id=ZOOM_ACCOUNT_ID, client_id=ZOOM_CLIENT_ID, client_secret=ZOOM_CLIENT_SECRET)

app = ZoomApp(client, transcriber=transcriber)
