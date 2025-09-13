from argparse import ArgumentParser, Namespace
import os

class CAS:
    def __init__(self, args: Namespace):
        if args.cas_type == "in-mem":
            from in_mem_cas import InMemoryCAS
            self.cas = InMemoryCAS()
        elif args.cas_type == "persistent":
            print("Persistent CAS not implemented yet.")
            exit(1)
        
        self.start_cli()

    def start_cli(self):
        print("Starting CAS cli. Type 'put <data>', 'get <hash>', or 'delete <hash>'. Ctrl+C to exit.")
        while(True):
            command = input(f"{os.getpid()}> ").strip()
            command_parts = command.split(" ", 2)
            if command_parts[0] == "put":
                data = command_parts[1]
                hash = self.cas.put(data)
                print(hash)
            elif command_parts[0] == "get":
                hash = command_parts[1]
                data = self.cas.get(hash)
                print(data)
            elif command_parts[0] == "delete":
                hash = command_parts[1]
                self.cas.delete(hash)
                print("Ok")

def main():
    parser = ArgumentParser(prog="CAS - Content Addressable Storage in Python")
    parser.add_argument(
        "-ct", "--cas-type", 
        type=str, choices=["in-mem", "persistent"], 
        default="in-mem", help="Type of CAS to use"
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