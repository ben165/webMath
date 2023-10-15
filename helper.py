#!/usr/bin/python3

import base64
import hashlib

saltTable = {
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
        saltTable[user]
    except:
        return False
    
    pw += saltTable[user]
    
    m = hashlib.sha256()
    m.update(pw.encode('utf-8'))

    if  (m.hexdigest() == pwTable[user]):
        return True
    return False



def sessionValid(session):
    if 'username' in session:
        return True
    return False
