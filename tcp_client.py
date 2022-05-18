import socket, tqdm, os, sys
from datetime import datetime
#import time


HOST = "localhost" # the ip address or hostname of the server, the receiver
PORT = 5001 
FILENAME = sys.argv[1] #C:\ziptest.zip
FILESIZE = os.path.getsize(FILENAME) 
BUFFER = int(sys.argv[2])


def client_tcp():
    try:
        blocks = 0
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        client_socket.connect((HOST, PORT))
  
        client_socket.send(f"{FILENAME}</>{FILESIZE}".encode())
        
        progress_bar = tqdm.tqdm(range(FILESIZE), f"Sending {FILENAME}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(FILENAME, "rb") as f:
            while True:
                data = f.read(BUFFER)
                if not data:
                    break

                client_socket.sendall(data) # OR client_socket.send(data)

                progress_bar.update(len(data))
                blocks = blocks + 1
    finally:
        # close the socket
        client_socket.close()
        #print(f"BLOCKS GENERATED: {blocks}")
        return blocks
        #print(f"{FILESIZE} / {BUFFER} = {int(FILESIZE/BUFFER)+1}")
        


if __name__ == "__main__":
    tstart = datetime.now()
    print(f"BLOCKS GENERATED: {client_tcp()}")
    tend = datetime.now()
    print (f"TIME ELAPSED: {(tend - tstart).total_seconds()*1000}")
    
    
