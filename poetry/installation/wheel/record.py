import csv

from io import StringIO
from pathlib import Path
from typing import Optional
from typing import Set
from typing import Union

from ._typing import GenericPath


class RecordSet:
    def __init__(self) -> None:
        self._records: Set[Record] = set()

    @property
    def content(self) -> str:
        content = StringIO()
        writer = csv.writer(content, delimiter=",", quotechar='"', lineterminator="\n")
        for record in sorted(self._records, key=lambda r: r.path.as_posix()):
            writer.writerow([record.path.as_posix(), record.hash_value, record.size])

        return content.getvalue()

    @classmethod
    def from_content(cls, content: Union[str, bytes]) -> "RecordSet":
        if isinstance(content, bytes):
            content = content.decode()

        content = StringIO(content)

        records = cls()
        reader = csv.reader(content, delimiter=",", quotechar='"', lineterminator="\n")
        for row in reader:
            records.add(Record(*row))

        return records

    def add(self, record: "Record") -> None:
        self._records.add(record)

    def remove(self, record: "Record") -> None:
        self._records.remove(record)

    def write_to(self, path: GenericPath) -> None:
        path.write_text(self.content)


class Record:
    def __init__(
        self,
        path: GenericPath,
        hash_value: Optional[str] = None,
        size: Optional[int] = None,
    ) -> None:
        self._path = Path(path)
        self._hash_value = hash_value
        self._size = size

    @property
    def path(self) -> Path:
        return self._path

    @property
    def hash_value(self) -> Optional[str]:
        return self._hash_value

    @property
    def size(self) -> Optional[int]:
        return self._size

    def __hash__(self) -> int:
        return hash(self._path.as_posix())

    def __repr__(self) -> str:
        return "{}({}, {}, {})".format(
            self.__class__.__name__, self._path.as_posix(), self._hash_value, self._size
        )
