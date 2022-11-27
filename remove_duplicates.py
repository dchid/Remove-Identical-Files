import hashlib
import json
import logging
import os
from argparse import ArgumentParser

logging.basicConfig(level="INFO")
logger = logging.getLogger()

def get_hash(fname):
    with open(fname, "rb") as fptr:
        res = hashlib.md5(fptr.read()).hexdigest()
    return res

def remove_duplicates(path, recursive):
    logger.info(f"scanning {path}")
    hashTable = {}
    for fname in os.listdir(path):
        fpath = os.path.join(path, fname)
        if os.path.isfile(fpath):
            fhash = get_hash(fpath)
            if fhash in hashTable:
                logger.info(f"removing {fpath}")
                os.remove(fpath)
                hashTable[fhash] += 1
            else:
                hashTable[fhash] = 0
        elif recursive:
            merge = remove_duplicates(fpath, recursive)
            hashTable.update(merge)
    return hashTable

if __name__ == "__main__":
    parser = ArgumentParser(description="remove duplicates files")
    cwd = os.getcwd()
    parser.add_argument("-p", "--path", required=False, default=cwd)
    parser.add_argument("-r",
            "--recursive",
            required=False,
            default=False,
            const=True,
            action='store_const'
    )
    args = parser.parse_args()
    hashes = remove_duplicates(path=args.path, recursive=args.recursive)
    with open("hashes.json", "w") as fptr:
        json.dump(hashes, fptr,indent=2)
    
