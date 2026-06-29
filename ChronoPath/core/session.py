from copy import deepcopy
from typing import Any


class SessionState:
    def __init__(self, initial: dict[str, Any] | None = None):
        self._data: dict[str, Any] = dict(initial or {})

    def set(self, key: str, value: Any) -> None:
        self._data[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def merge(self, values: dict[str, Any]) -> None:
        self._data.update(values)

    def to_dict(self) -> dict[str, Any]:
        return deepcopy(self._data)
