import os
import sys

from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

load_dotenv(os.path.join(BASE_DIR, ".env"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "music_project.settings")

try:
    application = get_wsgi_application()
except Exception as e:
    import traceback

    print("\n--- WSGI INITIALIZATION FAILED ---")
    traceback.print_exc()
    raise e
