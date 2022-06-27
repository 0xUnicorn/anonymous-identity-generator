import subprocess
import uuid
import hashlib
import string
import random
import json
import os


_DEFAULT_CONFIG = {
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


def _generate_md5() -> str:
    """Generate a MD5 Hash based on an UUID4.
    """
    random = str(uuid.uuid4()).encode()
    return hashlib.md5(random).hexdigest()


def generate_username(chars: int) -> str:
    """Generate a username with specified amount of chars.
    """
    if chars < 1 or chars > 32:
        raise ValueError("Username can only be 1-32 chars long")
    return _generate_md5()[:chars]


def generate_email(domain: str, chars: int, prefix: str = '') -> str:
    """Generate an email with provided domain name.
    """
    md5_hash = _generate_md5()
    email = f'{md5_hash[:chars]}@{domain}'
    if prefix:
        email = f'{prefix}-{email}'
    return email


def _get_all_ascii_characters():
    """Returns a list of all ascii characters.
    """
    black_list = ["'", '`']
    all_chars = list(string.ascii_letters + string.digits + string.punctuation)
    return [char for char in all_chars if not char in black_list]


def generate_password(chars: int) -> str:
    """Generates a random password with specified length.
    """
    characters = _get_all_ascii_characters()
    random.shuffle(characters)
    return ''.join(random.choices(characters, k=chars))


def copy_to_clipboard(element: str, clipboard: str) -> bool:
    """Saves element to clipboard if 'xclip' is installed.

    Param:
        clipboard: Can either be 'p'(primary) or 'c'(clipboard)
    """
    cmd = f"echo -n '{element}' | xclip -sel {clipboard}"
    result = subprocess.run(args=cmd,
                            shell=True,
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)
    if not result.returncode == 0:
        return False
    return True


def print_stdout(username: str = '',
                 email: str = '',
                 password: str = '',
                 pass_clip: bool = False,
                 email_clip: bool = False) -> None:
    """Prints the result to stdout.
    """
    print(f'[+] Username({len(username)}): {username}')
    if email_clip:
        print(f'[+] Email [MIDDLE MOUSE]: {email}')
    else:
        print(f'[+] Email: {email} | [MISSING XCLIP!]')

    pass_len = len(password)
    if pass_clip:
        mask = ''.join(['*' for _ in range(pass_len)])
        print(f'[*] Password({pass_len}) [CLIPBOARD]: {mask}')
    else:
        print(f'[+] Password({pass_len}): {password} | [MISSING XCLIP!]')


def load_config(path: str) -> dict:
    """Loads config file into Python dicts.
    """
    try:
        with open(path) as cfg:
            try:
                cfg = json.load(cfg)
                if cfg:
                    return cfg
                return {}
            except json.JSONDecodeError as ex:
                print(f'[!] Fatal error in config file: {path}')
                print(ex)
                exit(1)
    except FileNotFoundError:
        return {}


def get_configs() -> dict:
    """Combines default and user configs with priority for userconfig.
    """
    user_home = os.path.expanduser('~')
    user_cfg = load_config(f'{user_home}/.config/anonidgen/config.json')
    cfg = _DEFAULT_CONFIG.copy()
    for key in _DEFAULT_CONFIG:
        if key in user_cfg and user_cfg[key]:
            cfg[key].update(user_cfg[key])
    return cfg


def main() -> None:
    cfg = get_configs()
    username = generate_username(cfg['username'].get('chars'))
    email = generate_email(
        domain=cfg['email'].get('domain'),
        chars=cfg['email'].get('chars'),
        prefix=cfg['email'].get('prefix'))
    password = generate_password(cfg['password'].get('chars'))
    email_clip = copy_to_clipboard(email, 'p')
    pass_clip = copy_to_clipboard(password, 'c')
    print_stdout(username, email, password, pass_clip, email_clip)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass

