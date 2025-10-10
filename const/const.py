from enum import Enum


class Const(Enum):
    OK = "Ok"
    BASE_DIR = "./objects"
    BASE_META_DIR = "./metadata"
    CHUNK_SIZE = 500*1024  # 500KB