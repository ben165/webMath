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
  line-height: 1.75;
  font-size: 1.25em;
  max-width: 70ch;
  padding: 3em 1em;
  margin: auto;}
</style>
</head>
<body>
"""

TAIL = "</body></html>"


hashTable = {
    "jakob": "rP+P6LOUG8iDWLZ44L9P10Psj",
    "benjamin": "SpNJrACJAFUHsEe7Q57tAteMV"
}

pwTable = {
    "jakob": "03c2d2d6ac2b18bef970ed2b9d26a42cc842d9e1c3d61f03060dd76e137bc8b0",
    "benjamin": "2ec8de72b6068a82cea6c2a0b3675fbc6ebf475fc6e892cce8aa7d9a9d9d2d51"
}


def checkLogin(pw, user):

    if len(pw) < 1 or len(user) < 1:
        return False

    try:
        hashTable[user]
    except:
        return False
    
    pw = pw + hashTable[user]
    
    m = hashlib.sha256()
    m.update(pw.encode('utf-8'))

    if  (m.hexdigest() == pwTable[user]):
        return True
    return False



def sessionValid(session):
    if 'username' in session:
        return True
    return False
