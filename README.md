# Anonymous Identity Generator

## Intro

Obfuscate your online identity using anonymous usernames/emails and generate them along with a complex password.

The concept is based on password managers, for remembering both complex passwords and usernames/emails.

Due to common restrictions on username length and characters, the primary method will be a md5 hash sliced in half.

For emails you would need a catch all address on your domain or a 3rd party provider like [SimpleLogin](https://simplelogin.io) or [AnonAddy](https://anonaddy.com) due to obvious reasons.

## Installation

```bash
git clone https://github.com/0xUnicorn/anonymous-identity-generator.git
cd anonymous-identity-generator
pip install .
```

### Requirements

- python3.10

### Recommended

- xclip (For copying password to clipboard.)

#### APT based distro

```bash
sudo apt update && sudo apt install xclip
```

#### Pacman based distro

```
sudo pacman -Syu && sudo pacman -s xclip
```
## How to?

If you installed into a `virtualenv`/`venv`, remember to activate it first.

```bash
$ anonidgen

[+] Username(12): 76d766d16b44
[+] Email [MIDDLE MOUSE]: test-58ef2a@example.com
[*] Password(32) [CLIPBOARD]: ********************************
```

## Customization

By default the `anonidgen._DEFAULT_CONFIG` will be used. If you would like to change the default values, you can do so by creating the file `~/.config/anonidgen/config.json` and change the values.

The local `~/.config/anonidgen/config.json` takes priority and you don't have to overwrite all values, only the ones you need to.

**config.json**

```json
{
    "username": {
        "chars": 16
    },
    "email": {
        "domain": "guerillamail.com",
        "chars": 12,
        "prefix": ""
    },
    "password": {
        "chars": 32
    }
}
```

