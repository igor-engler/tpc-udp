import socket
import tqdm
import os

SEPARATOR = "</>"
BUFFER = 4096 # send 4096 bytes each time step
HOST = "192.168.1.78" # the ip address or hostname of the server, the receiver
PORT = 5001 
FILENAME = r"C:\ziptest.zip"
FILESIZE = os.path.getsize(FILENAME) 


if __name__ == "__main__":
    # create the client socket
    s = socket.socket()
    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print(f"[+] Connecting to {HOST}:{PORT}")
    #connect() espera um endereço do par(host, port) para se conectar o socket
    #aquele endereço removo
    s.connect((HOST, PORT))
    print("[+] Connected.")

    # send the filename and filesize
    s.send(f"{FILENAME}{SEPARATOR}{FILESIZE}".encode())

    # start sending the file
    progress_bar = tqdm.tqdm(range(FILESIZE), f"Sending {FILENAME}", unit="B", unit_scale=True, unit_divisor=BUFFER)
    with open(FILENAME, "rb") as f:
        while True:
            # read the bytes from the file
            data = f.read(BUFFER)
            if not data:
                # file transmitting is done
                break
            # we use sendall to assure transimission in 
            # busy networks
            s.sendall(data) # OR s.send(data)

            # update the progress bar
            progress_bar.update(len(data))
    # close the socket
    s.close()
