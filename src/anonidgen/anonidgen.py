import subprocess
import uuid
import hashlib
import string
import random


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


def generate_email(domain: str, length: int, prefix: str = '') -> str:
    """Generate an email with provided domain name.
    """
    md5_hash = _generate_md5()
    email = f'{md5_hash[:length]}@{domain}'
    if prefix:
        email = f'{prefix}-{email}'
    return email


def _get_all_ascii_characters():
    """Returns a list of all ascii characters.
    """
    black_list = ["'", '`']
    all_chars = list(string.ascii_letters + string.digits + string.punctuation)
    return [char for char in all_chars if not char in black_list]


def generate_password(length: int) -> str:
    """Generates a random password with specified length.
    """
    characters = _get_all_ascii_characters()
    random.shuffle(characters)
    return ''.join(random.choices(characters, k=length))


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


def main() -> None:
    username = generate_username(12)
    email = generate_email('example.com', length=6, prefix='test')
    email_clip = copy_to_clipboard(email, 'p')
    password = generate_password(32)
    pass_clip = copy_to_clipboard(password, 'c')
    print_stdout(username, email, password, pass_clip, email_clip)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass

