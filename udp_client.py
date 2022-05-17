import socket, time, os, sys, tqdm
from datetime import datetime

HOST = "localhost"
PORT = 5005
BUFFER = 500
FILENAME = sys.argv[1]
FILESIZE = os.path.getsize(FILENAME) 


def client_udp():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #sock.sendto(FILENAME.encode(), (UDP_IP, UDP_PORT))
        sock.sendto(f"{FILENAME}</>{FILESIZE}".encode(), (HOST, PORT))
        #print(file_name)

        f = open(FILENAME, "rb")
        data = f.read(BUFFER)

        progress_bar = tqdm.tqdm(range(FILESIZE), f"Sending {FILENAME}", unit="B", unit_scale=True, unit_divisor=1024)
        while(data):
            if(sock.sendto(data, (HOST, PORT))):
                data = f.read(BUFFER)
                progress_bar.update(len(data))
                #time.sleep(0.005) # Give receiver a bit time to save
    finally:
        sock.close()
        f.close()

if __name__ == "__main__":
    tstart = datetime.now()
    client_udp()
    tend = datetime.now()
    print (tend - tstart)