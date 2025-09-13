# Content Addressable Storage (CAS)
This repo contains Content Addressable Storage implementation from scratch in Python.

# Todo
- [ ] In-memory CAS
- [ ] Persistent CAS
- [ ] Chunk based storage for large files
- [ ] CLI to interact with the CAS

# Theory
Content-addressable storage (CAS) is a technique in which instead of identifying the files based on names/path, we use the hash function over every byte of the file content to calculate its address. It also helps in deduplication of files as two files with the same content will have the same hash value i.e <b><i>H(x) = H(x)</i></b> and hence same address.

# About In-memory CAS


# About Persistent CAS

# About Chunk based storage for large files

# CLI Impltementation

# References
[Content Addressable Storage - namvdo](https://namvdo.ai/content-addressable-storage)