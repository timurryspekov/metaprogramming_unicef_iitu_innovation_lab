import requests
import rsa
from binascii import b2a_hex
import cryptography
import os
import subprocess

# update version
__update_version__ = 'update_3.py'

user_name = 'Alikhan'
user_password = 'my_super_password'

# api urls
base_url = 'http://127.0.0.1:5000/'
get_key_url = base_url + 'api/v1.0/get_key'
get_file_url = base_url + 'api/v1.0/get_file'
get_all_update_files_url = base_url + 'api/v1.0/get_all_update_files'


def get_key(url, user_name):
    # Get public key from server by user name
    params = {'name': user_name}
    res = requests.get(url=url, json=params)
    keys = res.json()
    try:
        return rsa.PublicKey(n=keys['n'], e=keys['e'])
    except:
        pass


def get_file(url, user_name, user_password, public_key, file_name):
    # Encrypt user password using public key
    encrypted_password = rsa.encrypt(bytes(user_password, 'utf-8'), public_key)
    encrypted_password = b2a_hex(encrypted_password)
    # constructing params for request
    params = {'name': user_name,
              'password': encrypted_password,
              'file_name': file_name}
    res = requests.get(url, json=params)
    if res.content:
        encrypted_file, decrypted_file = f'encrypted_{file_name}', file_name
        # Write encrypted file
        with open(encrypted_file, 'wb') as f:
            f.write(res.content)
        # Decrypt file
        key = cryptography.gethash(user_password)
        cryptography.decrypt_file(key, encrypted_file, decrypted_file)
        # Remove encrypted file
        os.remove(encrypted_file)
        return decrypted_file


def mount_update(update_name):
    current_file = __file__

    with open(current_file, 'r') as f:
        lines = f.readlines()
        # Mount target code
        begin, end = lines.index(
            '# token 1 begin\n'), lines.index('# token 1 end\n')
        # Change info about update version
        version_line = lines.index('# update version\n') + 1
        lines[version_line] = f"__update_version__ = '{update_name}'\n"
        with open(update_name, 'r') as f:
            lines[begin + 1: end] = [f.read() + '\n']
        with open(__file__, 'w') as f:
            f.write(''.join(lines))
            os.remove(update_name)


def get_all_update_files(url):
    res = requests.get(url)
    if 'update_files' in res.json():
        files = sorted(res.json()['update_files'])
        return files


def update(get_key_url, get_file_url, user_name, user_password):
    all_updates = get_all_update_files(get_all_update_files_url)
    if all_updates:
        last_update = all_updates[-1]
        if str(__update_version__) < last_update:
            # Need to update
            public_key = get_key(get_key_url, user_name)
            update_file_name = get_file(
                get_file_url, user_name, user_password, public_key, last_update)
            mount_update(update_file_name)
            subprocess.call(f"/usr/bin/python3 {__file__}", shell=True)
            return True

is_updated = False
try:
    is_updated = update(get_key_url, get_file_url, user_name, user_password)
except Exception as e:
    pass

if is_updated:
    exit()



# Main program

# token 1 begin
print('update #3')

# token 1 end

