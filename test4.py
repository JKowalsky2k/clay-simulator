import json

with open("settings/settings.json") as settings_file:
    settings = json.load(settings_file)

print(f'{settings["clay_size"]["max"] = }')