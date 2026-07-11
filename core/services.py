from dataclasses import dataclass
from typing import Generic, Protocol, TypeVar

from shared.dataClass import appConfig, fileEntry

T = TypeVar("T")


class ServiceError(Exception):
    pass


class ScanAlreadyCompletedError(ServiceError):
    pass


class NoEntriesError(ServiceError):
    pass


class ScanExecutionError(ServiceError):
    pass


class HashExecutionError(ServiceError):
    pass


@dataclass
class ServiceResult(Generic[T]):
    ok: bool
    value: T | None = None
    error: ServiceError | None = None

    @staticmethod
    def success(value: T | None = None) -> "ServiceResult[T]":
        return ServiceResult(ok=True, value=value)

    @staticmethod
    def failure(error: ServiceError) -> "ServiceResult[T]":
        return ServiceResult(ok=False, error=error)


class ScannerPort(Protocol):
    def scan_directory(self, root_path: str) -> list[fileEntry]:
        ...


class HasherPort(Protocol):
    def hash_entries(self, entries: list[fileEntry]) -> None:
        ...


class RepositoryPort(Protocol):
    def save_entries(self, entries: list[fileEntry]) -> None:
        ...

    def get_all_entries(self) -> list[fileEntry]:
        ...


class ConfigPort(Protocol):
    def get(self) -> appConfig:
        ...

    def set_scan_completed(self) -> None:
        ...

    def set_scan_pending(self) -> None:
        ...


class FileProcessingService:
    def __init__(
        self,
        scanner: ScannerPort,
        hasher: HasherPort,
        repository: RepositoryPort,
        config: ConfigPort,
    ):
        self.scanner = scanner
        self.hasher = hasher
        self.repository = repository
        self.config = config

    def scan(self) -> ServiceResult[list[fileEntry]]:
        cfg = self.config.get()
        if cfg.isScanCompleted:
            return ServiceResult.failure(ScanAlreadyCompletedError("Scan already completed"))

        self.config.set_scan_pending()
        try:
            entries = self.scanner.scan_directory(cfg.scanDir)
            if not entries:
                return ServiceResult.failure(NoEntriesError("No hay entradas para guardar"))

            self.repository.save_entries(entries)
            self.config.set_scan_completed()
            return ServiceResult.success(entries)
        except ServiceError as error:
            return ServiceResult.failure(error)
        except Exception as error:
            return ServiceResult.failure(ScanExecutionError(str(error)))

    def sync(self) -> ServiceResult[list[fileEntry]]:
        try:
            entries = self.repository.get_all_entries()
            return ServiceResult.success(entries)
        except Exception as error:
            return ServiceResult.failure(ScanExecutionError(str(error)))

    def hash(self) -> ServiceResult[list[fileEntry]]:
        sync_result = self.sync()
        if not sync_result.ok:
            return ServiceResult.failure(sync_result.error or HashExecutionError("Sync failed"))

        entries = sync_result.value or []
        if not entries:
            return ServiceResult.failure(NoEntriesError("No hay entradas para hashear"))

        try:
            self.hasher.hash_entries(entries)
            self.repository.save_entries(entries)
            return ServiceResult.success(entries)
        except Exception as error:
            return ServiceResult.failure(HashExecutionError(str(error)))
