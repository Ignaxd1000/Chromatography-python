import json
from pathlib import Path

from dataClass import appConfig


class Config:

    CONFIG_PATH = Path("../../assets/conf.json")

    def __init__(self):

        if self.CONFIG_PATH.exists():
            self.cfg = self.load()
        else:
            self.cfg = self.createDefault()

    def load(self) -> appConfig:

        with open(self.CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        return appConfig(
            dbPath=data["dbPath"],
            scanDir=data["scanDir"],
            isScanCompleted=data["isScanCompleted"]
        )

    def edit(self, cfg: appConfig) -> None:

        with open(self.CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "dbPath": cfg.dbPath,
                    "scanDir": cfg.scanDir,
                    "isScanCompleted":cfg.isScanCompleted
                },
                f,
                indent=4,
                ensure_ascii=False
            )

        self.cfg = cfg

    def createDefault(self) -> appConfig:

        cfg = appConfig(
            dbPath="",
            scanDir="",
            isScanCompleted=False
        )

        self.edit(cfg)

        return cfg