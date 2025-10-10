from argparse import ArgumentParser, ArgumentTypeError, Namespace
import os
from pprint import pprint

from utils.utils import if_file, load_file


class CAS:
    def __init__(self, args: Namespace):
        self.args = args
        if self.args.cas_type == "in-mem":
            from in_mem_cas import InMemoryCAS
            self.cas = InMemoryCAS()
        elif self.args.cas_type == "persistent":
            from persistent_cas import PersistentCAS
            self.cas = PersistentCAS()
        elif self.args.cas_type == "chunk":
            from chunk_based_cas import ChunkBasedCAS
            self.cas = ChunkBasedCAS(chunk_size=self.args.chunk_size)
        else:
            raise ArgumentTypeError("Invalid CAS type")
        
        self.start_cli()

    def start_cli(self):
        print(f"Starting {self.args.cas_type.capitalize()} CAS cli. Type 'put <data>', 'get <hash>', or 'delete <hash>'. Ctrl+C to exit.")
        while(True):
            command = input(f"{os.getpid()}> ").strip()
            command_parts = command.split(" ", 2)
            command = command_parts[0].lower()
            if command == "put":
                data = command_parts[1]
                if if_file(data):
                    if  self.args.cas_type != "chunk":
                        data = load_file(data)
                    else: 
                        data = data  # chunk-based cas expects file path
                if not data:
                    print(None)
                else:
                    hash = self.cas.put(data)
                    print(hash)
            elif command == "get":
                hash = command_parts[1]
                data = self.cas.get(hash)
                print(data)
            elif command == "delete":
                hash = command_parts[1]
                self.cas.delete(hash)
                print("Ok")
            elif command == "clear":
                os.system("cls" if os.name == "nt" else "clear")
            elif command == "exit":
                exit(0)

def main():
    parser = ArgumentParser(prog="CAS - Content Addressable Storage in Python")
    parser.add_argument(
        "-ct", "--cas-type", 
        type=str, choices=["in-mem", "persistent", "chunk"], 
        default="in-mem", help="Type of CAS to use"
    )
    parser.add_argument(
        "-cs", "--chunk-size",
        type=int, default=100*1024, help="Chunk size in bytes (only for chunk-based CAS)"
    )
    parser.add_argument(
        "-hf", "--hash-function",
        type=str, choices=["sha256", "sha512"],
        default="sha256", help="Hash function to use"
    )
    args = parser.parse_args()
    CAS(args)
    
if __name__ == "__main__":
    exit(main())