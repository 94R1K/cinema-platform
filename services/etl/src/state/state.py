from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from state.storage import BaseStorage


@dataclass
class Checkpoint:
    modified: datetime
    id: UUID | None = None


class ETLState:
    """Класс для работы с состоянием ETL."""

    def __init__(self, storage: BaseStorage) -> None:
        self.storage = storage
        self.data = storage.retrieve_state()

    def set_checkpoint(
        self,
        key: str,
        checkpoint: Checkpoint | None,
    ) -> None:
        if checkpoint is None:
            return

        self.data[key] = {
            "modified": checkpoint.modified.isoformat(),
            "id": str(checkpoint.id) if checkpoint.id else None,
        }

        self.storage.save_state(self.data)

    def get_checkpoint(
        self,
        key: str,
    ) -> Checkpoint | None:
        data = self.data.get(key)

        if data is None:
            return None

        return Checkpoint(
            modified=datetime.fromisoformat(data["modified"]),
            id=UUID(data["id"]) if data["id"] else None,
        )
