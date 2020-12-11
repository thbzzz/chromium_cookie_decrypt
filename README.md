# Chromium cookie decrypt

CLI utility to decrypt cookies saved in chromium's database on Linux/OS X.

## Installation

Simply clone the git repo and install requirements.

```bash
git clone https://github.com/thbzzz/chromium_cookie_decrypt.git
cd chromium_cookie_decrypt
pip3 install -r requirements.txt --user
```

## Usage

```
chromium_cookie_decrypt.py <sqlite> <name> [<domain>]
```

## Examples

```
$ chromium_cookie_decrypt.py ~/.config/chromium/Default/Cookies PHPSESSID
+-----------+-----------------------------+-----------------------------+
| name      | domain                      | value                       |
+-----------+-----------------------------+-----------------------------+
| PHPSESSID | example.com                 | <value>                     |
| PHPSESSID | thegame.com                 | <value>                     |
+-----------+-----------------------------+-----------------------------+
```

```
$ chromium_cookie_decrypt.py ~/.config/chromium/Default/Cookies user_session github.com
+--------------+------------+--------------------------------------------------+
| name         | domain     | value                                            |
+--------------+------------+--------------------------------------------------+
| user_session | github.com | <value>                                          |
+--------------+------------+--------------------------------------------------+
```

## Credits

The crypto stuff inside this script doesn't come from my mind, but from [this StackOverflow answer](https://stackoverflow.com/questions/23153159/decrypting-chromium-cookies/23727331#23727331).
