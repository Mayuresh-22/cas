'''
Simple in-memory content addressable storage implementation.
'''
from hashlib import sha256

class InMemoryCAS:
    def __init__(self):
        self.store = {}

    def put(self, data: str) -> str:
        hasher = sha256()
        hasher.update(bytes(data, encoding="utf-8"))
        hexhash = hasher.hexdigest()
        # check if hash already exists (deduplication)
        if hexhash not in self.store:
            self.store[hexhash] = data
        return hexhash

    def get(self, hash: str) -> str | None:
        return self.store.get(hash, None)

    def delete(self, hash: str) -> None:
        del self.store[hash]