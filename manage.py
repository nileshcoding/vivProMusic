import os
import sys

from dotenv import load_dotenv


def main():
    """Run administrative tasks."""
    load_dotenv()

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "music_project.settings")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    try:
        execute_from_command_line(sys.argv)
    except Exception as e:
        import traceback

        print("\n--- DJANGO CRASH DETECTED ---")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
