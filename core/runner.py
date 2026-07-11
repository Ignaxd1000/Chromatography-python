from adapters import ConfigAdapter, DatabaseRepositoryAdapter, HasherAdapter, ScannerAdapter
from shared.exceptions import scanAlreadyCompleted
from services import FileProcessingService, NoEntriesError, ScanAlreadyCompletedError


class runner:

    def __init__(self):
        self.config_adapter = ConfigAdapter()
        config = self.config_adapter.get()
        self.database_adapter = DatabaseRepositoryAdapter(config.dbPath)
        self.service = FileProcessingService(
            scanner=ScannerAdapter(),
            hasher=HasherAdapter(),
            repository=self.database_adapter,
            config=self.config_adapter,
        )
        self.entries = []


    def scan(self):
        result = self.service.scan()
        if result.ok:
            self.entries = result.value or []
            return

        if isinstance(result.error, ScanAlreadyCompletedError):
            raise scanAlreadyCompleted()
        print(f"Ocurrió un problemin. {result.error}")


    def sync(self):
        result = self.service.sync()
        if result.ok:
            self.entries = result.value or []
            return
        print(f"Ocurrió un problemin. {result.error}")


    def hash(self):
        result = self.service.hash()
        if result.ok:
            self.entries = result.value or []
            return

        if isinstance(result.error, NoEntriesError):
            raise Exception("No hay entradas para hashear")
        print(f"Ocurrió un problemin. {result.error}")

        