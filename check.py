#!/usr/bin/env python3
from datetime import date
import mimetypes
import subprocess
import sys

ret = 0
year = str(date.today().year)

for line in subprocess.getoutput("git diff --name-status HEAD~").splitlines():
    status, path = line.split("\t", 1)

    # Skip deleted file
    if status == "D":
        continue

    # Skip renamed file
    if status == "R100":
        continue

    # Skip files not in scanned paths
    if not any(path.startswith(f"{x}/") for x in sys.argv[1].split(",")):
        continue

    # Skip non-text files
    if not mimetypes.guess_type("sample.html")[0].startswith("text/"):
        continue

    with open(path, "r") as f:
        # Read first 16 lines
        for x in f.read().splitlines()[:16]:
            if "Copyright" in x and year in x:
                break
        else:
            print(f"{path} is missing or has wrong copyright year")
            ret = 1

exit(ret)
