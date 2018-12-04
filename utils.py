import argon2
from argon2 import PasswordHasher
import secrets
import string
import time


def current_millis():
    """
    Gets the current time in milliseconds since the unix epoch
    """
    return int(round(time.time() * 1000))


def genSalt():
    """
    Generates a random printable salt from 32 to 128 characters long
    :return: the generated salt
    """
    return ''.join(secrets.choice(string.printable) for i in range(32, 128))


def hashPasswd(password, salt):
    """
    Hashes the provided password and salt
    :param password: the password to hash
    :param salt: the salt to merge with the password
    :return: the hashed secret
    """
    hasher = PasswordHasher()
    return hasher.hash(password + salt)

def checkHash(hash, secret):
    hasher = PasswordHasher()
    try:
        # so v1 re-hashed the password... argon2 doesn't make predictable hashes..2 hours wasted
        return hasher.verify(hash, secret)
    except Exception as e:
        return False
