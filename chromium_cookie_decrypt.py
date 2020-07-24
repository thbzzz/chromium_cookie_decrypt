#! /usr/bin/env python3
# source: https://stackoverflow.com/questions/23153159/decrypting-chromium-cookies/23727331#23727331

"""Chromium cookie decrypt
Usage:
  chromium_cookie_decrypt.py <sqlite> <name> [<host_key>]
"""

import sqlite3
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from docopt import docopt

def select_cookie(sqlite_path, cookie_name, cookie_domain=None):
    sqlite = sqlite3.connect(sqlite_path)
    c = sqlite.cursor()
    if cookie_domain:
        c.execute('SELECT encrypted_value FROM cookies WHERE name=? and host_key=?', (cookie_name,cookie_domain))
    else:
        c.execute('SELECT encrypted_value FROM cookies WHERE name=?', (cookie_name,))
    
    results = c.fetchone()
    if results:
        return results[0]
    else:
        return None

def decrypt_cookie(cookie_enc):
    # Function to get rid of padding
    def clean(x): 
        return x[:-x[-1]].decode('utf8')
    # Trim off the 'v10' that Chrome/ium prepends
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
    return clean(cipher.decrypt(cookie_enc))

if __name__ == "__main__":
    args = docopt(__doc__)
    
    cookie_encrypted = select_cookie(
        args["<sqlite>"],
        args["<name>"],
        args["<host_key>"]
    )

    if not cookie_encrypted:
        exit("cookie not found")

    cookie_decrypted = decrypt_cookie(cookie_encrypted)
    print(cookie_decrypted)
