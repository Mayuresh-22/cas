'''
Persistent content addressable storage implementation.
- we create a directory out of the hash i.e generated
- we use first one byte (2 chars) to create a first level directory
- we use next one byte (2 chars) to create a second level directory
- we use the rest of the hash as the filename
- we store the data in the file

This approach helps to avoid too many files in same directory as this  
affects search and retrieval performance.
'''

# USAGE:
# uv run .\cas.py -ct persistent
# put ./temp/temp.pdf

from hashlib import sha256
from os import path
import os
from typing import Optional

from const.const import Const


class PersistentCAS:
    def __init__(self, base_dir: str = Const.BASE_DIR.value):
        self.base_dir = base_dir
    
    def put(self, data: str) -> Optional[str]:
        hasher = sha256()
        hasher.update(bytes(data, encoding="utf-8"))
        hexhash = hasher.hexdigest()
        _path = self.hash_to_path(hexhash)
        _dir_path = path.dirname(_path)
        
        try:
            # create leaf and intermediate directories
            #  if absent
            if not path.exists(_dir_path):
                os.makedirs(_dir_path)
                with open(_path, "w") as f:
                    f.write(data)
            return hexhash
        except Exception:
            return None
        
    
    def get(self, hash: str) -> Optional[str]:
        try:
            with open(self.hash_to_path(hash), "r") as f:
                return f.read()
        except Exception:
            return None
    
    def delete(self, hash: str) -> Optional[str]:
        try:
            _path = self.hash_to_path(hash)
            # remove file and empty directories
            if path.isfile(_path):
                os.remove(_path)
                os.removedirs(path.dirname(_path))
            return Const.OK.value
        except Exception:
            return None
    
    def hash_to_path(self, hash: str) -> str:
        # 1 byte for first dir
        # 1 byte for second dir
        # remaining bytes for filename (no extension)
        dir1 = hash[:2]
        dir2 = hash[2:4]
        filename = hash[4:]
        return path.join(self.base_dir, dir1, dir2, filename)