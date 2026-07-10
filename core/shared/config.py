import json
from pathlib import Path

from dataClass import appConfig


class Config:

    CONFIG_PATH = Path("../../assets/conf.json")

    def __init__(self):

        if self.CONFIG_PATH.exists():
            self.args = self.load()
        else:
            self.args = self.createDefault()

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

        self.args = cfg

    def createDefault(self) -> appConfig:

        cfg = appConfig(
            dbPath="cases/chromatography.db",
            scanDir="",
            isScanCompleted=False
        )

        self.edit(cfg)

        return cfg
    
    def setScanCompleted(self):
        self.args.isScanCompleted = True
        self.edit(self.args)

    def setScanPending(self):
        self.args.isScanCompleted = False
        self.edit(self.args)