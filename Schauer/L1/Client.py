import os.path

import requests
from os import path

def send_file(host, path_to_file:str):
    host_post = host + '/upload'
    if os.path.exists(path_to_file):
        file = [('file',(path.basename(path_to_file),open(path_to_file,'rb'),'text/plain'))]
        requests.request("POST", host_post, files=file)
        return "File sended"
    else:
        return "File not found"

def get_file(host, file_name:str, line:int):
    host_get = host + '/'+file_name
    row = {'line':line}
    reque = requests.get(host_get, params=row)
    code = str(reque.status_code)
    if code != '200':
        print('Server error: ' + code)
        return int(code)
    else:
        resp = reque.json()['content']
        print(resp)
        return int(code)
if __name__ == "__main__":
    get_file('http://localhost:5002', 'Test.txt', 1)
    get_file('http://localhost:5002', 'Test.txt', 4)
    send_file('http://localhost:5002', './Test.txt')
