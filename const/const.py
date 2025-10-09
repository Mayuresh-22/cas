from enum import Enum


class Const(Enum):
    OK = "Ok"
    BASE_DIR = "./objects"
    BASE_META_DIR = "./metadata"
    CHUNK_SIZE = 512  # 512 bytes