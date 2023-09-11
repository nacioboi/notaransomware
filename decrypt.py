import os
from cryptography.fernet import Fernet

files = []

def find_files(dir=""):
    global files
    if dir != "":
        for i, (t, file, _) in enumerate(files):
            if t == "d" and file == dir:
                files[i][2] = True
    else:
        dir = os.getcwd()
    for file in os.listdir(dir):
        if file == "notaransomware.py" or file == "decrypt.py" or file == "thekey.key":
            continue
        print(f"found `{file}`...")
        file = f"{dir}\\{file}"
        if os.path.isfile(file):
            files.append(["f", file, False])
        elif os.path.isdir(file):
            files.append(["d", file, False])
        else:
            files.append(["?", file, False])

def find_more_files():
    global files
    for (t, file, found_already) in files:
        if t == "d" and not found_already:
            find_files(file)
            find_more_files()

find_files()
find_more_files()

with open("thekey.key", "rb") as f:
    key = f.read()

for (t, file, _) in files:
    if t == "?": print("something unexpected happened")
    if t != "f":
        continue  
    with open(file, "rb") as f:
        encrypted_contents = f.read()
    decrypted_contents = Fernet(key).decrypt(encrypted_contents)
    with open(file, "wb") as f:
        f.write(decrypted_contents)
    
