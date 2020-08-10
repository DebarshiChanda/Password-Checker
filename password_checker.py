import requests
import hashlib


def pass2hash(password):
    """
    Converts password to SHA-1 hashcode
    """
    h = hashlib.sha1()
    h.update(password.encode('utf-8'))
    hashed_password = h.hexdigest().upper()
    return hashed_password


def request_api_data(hashed_password):
    """
    Takes hashed password as input and returns the suffix and a list of suffixes with matching prefixes
    """
    prefix, suffix = hashed_password[:5], hashed_password[5:]
    url = "https://api.pwnedpasswords.com/range/" + prefix
    response = requests.get(url)
    suffix_list = [line.split(':') for line in response.text.splitlines()]
    return suffix, suffix_list


def match_suffix(suffix, suffix_list):
    """
    Matches suffix to the list of matching suffixes and returns if password was ever hacked
    """
    for tail, count in suffix_list:
        if tail == suffix:
            return f'Password breached {count} times'
    return 'Safe Password'

def check_password():
    password = input('Enter Password: ')
    hashed_password = pass2hash(password)
    suffix, suffix_list = request_api_data(hashed_password)
    result = match_suffix(suffix, suffix_list)
    print(result)

if __name__ == '__main__':
    check_password()