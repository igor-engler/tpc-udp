import socket, time, os, sys, tqdm
from datetime import datetime

HOST = "localhost"
PORT = 5001
FILENAME = sys.argv[1]
FILESIZE = os.path.getsize(FILENAME) 
BUFFER = int(sys.argv[2])

def g_client_udp():
    try:
        blocks = 0
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #sock.sendto(FILENAME.encode(), (UDP_IP, UDP_PORT))
        sock.sendto(f"{FILENAME}</>{FILESIZE}".encode(), (HOST, PORT))
        #print(file_name)

        f = open(FILENAME, "rb")
        data = f.read(BUFFER)

        ack = b'ack'
        progress_bar = tqdm.tqdm(range(FILESIZE), f"Sending {FILENAME}", unit="B", unit_scale=True, unit_divisor=1024)
        while(data): 
            if ack == b'ack':
                if(sock.sendto(data, (HOST, PORT))):
                    blocks = blocks + 1
                    data = f.read(BUFFER)
                    progress_bar.update(len(data))
                    ack=b'nack'
   
                ack, host = sock.recvfrom(BUFFER)
            else:
                while(ack!=b'ack'):
                    if(sock.sendto(data, (HOST, PORT))):
                        blocks = blocks + 1
                        data = f.read(BUFFER)
                        progress_bar.update(len(data))
                        ack, host = sock.recvfrom(BUFFER)
    finally:
        sock.close()
        f.close()
        return blocks

if __name__ == "__main__":
    tstart = datetime.now()
    print(f"BLOCKS GENERATED: {g_client_udp()}")
    tend = datetime.now()
    print (f"TIME ELAPSED: {(tend - tstart).total_seconds()*1000}")