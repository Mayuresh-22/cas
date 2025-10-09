"""
Chunk-based Content Addressable Storage (CAS) implementation.
- we expect text file as an input
- we break the file into fixed size chunks
- we create a directory out of the hash i.e generated (same as in-memory/persistent cas style)
- we generate a metadata object which contains the total size of the file and 
    hashes of all the chunks in order (so that we can replay them in order to get the original file)
"""

from hashlib import sha256
import json
from logging import warning
from os import path
from typing import Any, Optional, List
import os

from const.const import Const

class ChunkBasedCAS:
    def __init__(
        self, 
        base_dir: str = Const.BASE_DIR.value, 
        base_meta_dir: str = Const.BASE_META_DIR.value, 
        chunk_size: int = Const.CHUNK_SIZE.value
    ):
        self.base_dir = base_dir
        self.base_meta_dir = base_meta_dir
        self.chunk_size = chunk_size

    def get_chunks(self, file_obj: Any) -> str | Any:
        while True:
            chunk = file_obj.read(self.chunk_size)
            if not chunk:
                break
            yield chunk
    
    def put(self, file_path: str) -> Optional[str]:
        if not path.isfile(file_path):
            return None
        
        metadata = {
            "total_size": 0,
            "chunks": []
        }
        
        hashes = []
        with open(file_path, "r") as f:
            for chunk in self.get_chunks(f):
                if chunk_hash := self.put_persistent(str(chunk)):
                    hashes.append(chunk_hash)
                metadata["total_size"] += len(chunk)
                
        metadata["chunks"] = hashes
        
        return self.put_persistent(json.dumps(metadata), isMetadata=True)
        
    def put_persistent(self, data: str, isMetadata: bool = False) -> Optional[str]:
        # same from persistent cas
        hasher = sha256()
        hasher.update(bytes(data, encoding="utf-8"))
        hexhash = hasher.hexdigest()
        _path = self.hash_to_path(hexhash, isMetadata)
        _dir_path = path.dirname(_path)
        
        try:
            if not path.exists(_dir_path):
                os.makedirs(_dir_path)
                with open(_path, "w") as f:
                    f.write(data)
            return hexhash
        except Exception:
            return None

    def get(self, hash: str) -> Optional[str]:
        # we expect the hash to be of the metadata object
        try:
            raw_data = self.get_persistent(hash, isMetadata=True)
            if not raw_data:
                return None
            metadata = json.loads(raw_data)
            file_data = ""
            for chunk_hash in metadata["chunks"]:
                if chunk_data := self.get_persistent(chunk_hash):
                    file_data += chunk_data
            
            return file_data
        except Exception:
            return None
        
    def get_persistent(self, hash: str, isMetadata: bool = False) -> Optional[str]:
        try:
            with open(self.hash_to_path(hash, isMetadata), "r") as f:
                return f.read()
        except Exception:
            return None
    
    def delete(self, hash: str) -> Optional[str]:
        """
            Deletion in chunk-based CAS is not that straightforward.
            - we need to keeptrack of reference counts for each chunk
            - we can only delete a chunk it its reference count reaches zero
            
            TODO: you've to implement it someday, but not today
        """
        warning("Delete operation is not supported in ChunkBasedCAS")
        return None

    def hash_to_path(self, hash: str, isMetadata: bool = False) -> str:
        # 1 byte for first dir
        # 1 byte for second dir
        # remaining bytes for filename (no extension)
        dir1 = hash[:2]
        dir2 = hash[2:4]
        filename = hash[4:]
        return path.join(
            self.base_dir if not isMetadata else self.base_meta_dir, 
            dir1, 
            dir2, 
            filename
        )