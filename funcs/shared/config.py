import json
from dataClass import appConfig

def loadConfig() -> appConfig:
    with open("../../assets/conf.json", "r", encoding="utf8") as f:
        data = json.load(f)

    return appConfig(
        dbPath=data["dbPath"],
    )

config = loadConfig()