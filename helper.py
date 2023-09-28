#!/usr/bin/python3

import base64
import hashlib

HEAD = """<!doctype html>
<html lang="en">
<head>
<title>V 0.1</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0;" />
<style>
html {
  max-width: 70ch;
  padding: 3em 1em;
  margin: auto;
  line-height: 1.75;
  font-size: 1.25em;
}
</style>
</head>
<body>
"""

TAIL = "</body></html"

hashTable = {
    "jakob": "rP+P6LOUG8iDWLZ44L9P10Psj",
    "benjamin": "SpNJrACJAFUHsEe7Q57tAteMV"
}

pwTable = {
    "jakob": "03c2d2d6ac2b18bef970ed2b9d26a42cc842d9e1c3d61f03060dd76e137bc8b0",
    "benjamin": "2ec8de72b6068a82cea6c2a0b3675fbc6ebf475fc6e892cce8aa7d9a9d9d2d51"
}


def createHash(str1, user):
    try:
        hashTable[user]
    except:
        return "0000000000000000000000000000000"  # value cant be created. Login will fail.
    str1 += hashTable[user]
    m = hashlib.sha256()
    m.update(str1.encode('utf-8'))
    return m.hexdigest()


def getPw(user):
    try:
        return pwTable[user]
    except:
        return "0000000000000000000000000000001"  # value cant be created. Login will fail.
