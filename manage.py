#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from dotenv import load_dotenv


def main():
    """Run administrative tasks."""
    # 1. Load .env before anything else
    load_dotenv()

    # 2. Point to the settings in your music_project folder
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "music_project.settings")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # 3. Wrap in a broad try/except to catch silent crashes
    try:
        execute_from_command_line(sys.argv)
    except Exception as e:
        import traceback

        print("\n--- DJANGO CRASH DETECTED ---")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
