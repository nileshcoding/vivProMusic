# import os
# from django.core.wsgi import get_wsgi_application
# from dotenv import load_dotenv

# project_folder = os.path.expanduser('..')
# load_dotenv(os.path.join(project_folder, '.env'))

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music_project.settings')

# application = get_wsgi_application()
import os
import sys

from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

# 1. Add the current directory to sys.path to ensure imports work in production
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# 2. Load environment variables
load_dotenv(os.path.join(BASE_DIR, ".env"))

# 3. Set settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "music_project.settings")

try:
    application = get_wsgi_application()
except Exception as e:
    import traceback

    print("\n--- WSGI INITIALIZATION FAILED ---")
    traceback.print_exc()
    raise e
