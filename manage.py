#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import subprocess
from pathlib import Path


CLIENT_DIR = Path(__file__).resolve().parent / "client"


def run_frontend_build():
    """Run npm install and build safely."""
    if not CLIENT_DIR.exists():
        print("⚠️ Client directory not found. Skipping frontend build.")
        return

    try:
        print("📦 Installing frontend dependencies...")
        subprocess.run(
            ["npm", "install"],
            cwd=CLIENT_DIR,
            check=True,
            shell=os.name == "nt",
        )

        print("🏗️ Building frontend...")
        subprocess.run(
            ["npm", "run", "build"],
            cwd=CLIENT_DIR,
            check=True,
            shell=os.name == "nt",
        )

    except subprocess.CalledProcessError as e:
        print("❌ Frontend build failed")
        sys.exit(e.returncode)


def main():
    """Run administrative tasks."""

    # Only run frontend build for runserver / collectstatic
    if len(sys.argv) > 1 and sys.argv[1] in {"runserver", "collectstatic"}:
        run_frontend_build()

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
