from flask import Flask, jsonify, abort, request, send_file
import rsa
import cryptography
from binascii import a2b_hex
import os

app = Flask(__name__)

dict_users = {}

# Create directory for updates files if does not exist
updates_dir = os.path.join(os.getcwd(), 'updates_files')
try:
    os.mkdir(updates_dir)
except:
    pass

@app.route('/api/v1.0/get_all_update_files', methods=['GET', 'POST'])
def get_all_update_files():
    try:
        result = {'update_files': sorted(os.listdir(updates_dir))}
        return jsonify(result), 201
    except:
        pass
    return ''

@app.route('/api/v1.0/get_key', methods=['GET', 'POST'])
def get_key():
    if not request.json or not 'name' in request.json:
        abort(400)

    public_key, private_key = rsa.newkeys(1024)
    dict_users[str(request.json['name'])] = private_key
    results = {'e':  public_key.e, 'n': public_key.n}
    return jsonify(results), 201


@app.route('/api/v1.0/get_file', methods=['GET', 'POST'])
def get_file():

    if not request.json or not 'name' in request.json or not 'password' in request.json:
        abort(400)

    # Check for updates
    try:
        updates = os.listdir(updates_dir)
        if updates:
            user_name = request.json['name']
            decrypted_password = a2b_hex(request.json['password'])
            update_name = request.json['file_name']
            update_path = os.path.join(updates_dir, update_name)
            encrypted_file_path = os.path.join(updates_dir, f'{update_name}_{user_name}.py')
            private_key = dict_users[user_name]
            decrypted_pasword = rsa.decrypt(decrypted_password, private_key).decode('utf-8')
            key = cryptography.gethash(str(decrypted_pasword))
            cryptography.encrypt_file(key, update_path, encrypted_file_path)
            result = send_file(encrypted_file_path)
            os.remove(encrypted_file_path)
            return result, 201
    except Exception as e:
        print(e)
        pass
    return ''


if __name__ == "__main__":
    app.run()
