import json

from flask import request

from loggerthyst import info


def _load_settings():
    try:
        with open("settings.json", "r") as f:
            settings = json.load(f)
        info("Settings loaded successfully")
        return settings
    except FileNotFoundError:
        info("Settings file not found, creating a new one with default settings")
        settings = {
            "flip_video": False,
            # Add more settings here as needed
        }
        with open("settings.json", "w") as f:
            json.dump(settings, f, indent=4)
        return settings


def _update_settings(settings):
    settings.update(
        request.get_json()
    )  # Update settings with data from the POST request
    with open("settings.json", "w") as f:
        json.dump(settings, f, indent=4)
    return settings
