from __future__ import annotations

import copy
import hashlib
import json
import time
from typing import Any


class ResponseCache:
    def __init__(self, ttl: int = 30) -> None:
        self.ttl = max(0, ttl)
        self._items: dict[str, tuple[float, dict[str, Any]]] = {}
        self._scopes: dict[str, str] = {}

    def _key(self, tool_name: str, arguments: dict[str, Any]) -> str:
        encoded = json.dumps({"tool": tool_name, "arguments": arguments}, sort_keys=True, ensure_ascii=False)
        return hashlib.sha1(encoded.encode("utf-8")).hexdigest()

    def get(self, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any] | None:
        if self.ttl <= 0:
            return None
        key = self._key(tool_name, arguments)
        item = self._items.get(key)
        if item is None:
            return None
        expires_at, payload = item
        if expires_at < time.time():
            self._items.pop(key, None)
            return None
        return copy.deepcopy(payload)

    def set(self, tool_name: str, arguments: dict[str, Any], payload: dict[str, Any]) -> None:
        if self.ttl <= 0:
            return
        key = self._key(tool_name, arguments)
        self._items[key] = (time.time() + self.ttl, copy.deepcopy(payload))
        scope = arguments.get("scope", "")
        self._scopes[key] = scope if isinstance(scope, str) else ""

    def invalidate_scope(self, scope: str) -> None:
        if not scope:
            self._items.clear()
            return
        selected: list[str] = []
        marker = json.dumps(scope, ensure_ascii=False)
        for key, (_expires_at, payload) in self._items.items():
            if self._scopes.get(key) == scope or marker in json.dumps(payload, ensure_ascii=False):
                selected.append(key)
        for key in selected:
            self._items.pop(key, None)
            self._scopes.pop(key, None)

    def size(self) -> int:
        now = time.time()
        expired = [key for key, (expires_at, _payload) in self._items.items() if expires_at < now]
        for key in expired:
            self._items.pop(key, None)
            self._scopes.pop(key, None)
        return len(self._items)
