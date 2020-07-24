# Chromium cookie decrypt

CLI utility to decrypt a cookie saved in chromium's database on Linux/OS X.

## Installation

Simply clone the git repo and install requirements.

```bash
git clone https://github.com/thbzzz/chromium_cookie_decrypt.git
cd chromium_cookie_decrypt
pip3 install -r requirements.txt --user
```

## Usage

```
chromium_cookie_decrypt.py <sqlite> <name> [<host_key>]
```

## Credits
The crypto stuff inside this script doesn't come from my mind, but from [this StackOverflow answer](https://stackoverflow.com/questions/23153159/decrypting-chromium-cookies/23727331#23727331).
