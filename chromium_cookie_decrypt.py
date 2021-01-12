#!/usr/bin/env python3
# source: https://stackoverflow.com/questions/23153159/decrypting-chromium-cookies/23727331#23727331

"""Chromium cookie decrypt
Usage:
  chromium_cookie_decrypt.py <sqlite> <name> [<domain>]
"""

import sqlite3

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from docopt import docopt

from prettytable import PrettyTable


def select_cookies(sqlite_path, cookie_name, cookie_domain=None):
    """Select encrypted cookies' name,domain,value in database.

    Args:
        sqlite_path (str): Chromium cookies sqlite file.
        cookie_name (str): Cookie to retrieve.
        cookie_domain (str, optional): Filter selected cookies by domain.
            Defaults to None.

    Returns:
        list: List of tuples representing retrieved cookies.
    """
    sqlite = sqlite3.connect(sqlite_path)
    cursor = sqlite.cursor()
    query = "SELECT name, host_key, encrypted_value FROM cookies WHERE name=?"

    if cookie_domain:
        query += " and host_key=?"
        cursor.execute(query, (cookie_name, cookie_domain))
    else:
        cursor.execute(query, (cookie_name,))

    return cursor.fetchall()


def decrypt_cookie(cookie_enc):
    """Decrypt an encrypted cookie.

    Args:
        cookie_enc (tuple): name,domain,encrypted_value.

    Returns:
        tuple: name,domain,decrypted_value.
    """
    # Function to get rid of padding
    def clean(x):
        return x[:-x[-1]].decode()

    # Trim off the 'v10' that Chrome/ium prepends
    name, domain, cookie_enc = cookie_enc
    cookie_enc = cookie_enc[3:]

    # Default values used by both Chrome and Chromium in OSX and Linux
    salt = b'saltysalt'
    iv = b' ' * 16
    length = 16

    # On Mac, replace MY_PASS with your password from Keychain
    # On Linux, replace MY_PASS with 'peanuts'
    # my_pass = MY_PASS
    my_pass = "peanuts".encode("utf8")

    # 1003 on Mac, 1 on Linux
    iterations = 1
    key = PBKDF2(my_pass, salt, length, iterations)
    cipher = AES.new(key, AES.MODE_CBC, IV=iv)

    return (name, domain, clean(cipher.decrypt(cookie_enc)))


if __name__ == "__main__":
    args = docopt(__doc__)

    cookies_encrypted = select_cookies(
        args["<sqlite>"],
        args["<name>"],
        args["<domain>"]
    )

    cookies_decrypted = [decrypt_cookie(c) for c in cookies_encrypted]

    table = PrettyTable()
    table.field_names = ["name", "domain", "value"]
    [table.add_row(c) for c in cookies_decrypted]
    table.align = "l"
    print(table)
