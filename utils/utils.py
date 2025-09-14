import os
from typing import Optional


def load_file(path: str) -> Optional[str]:
    """File loader"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return None
    
def if_file(path: str) -> bool:
    """Check if file exists"""
    return os.path.isfile(path)
