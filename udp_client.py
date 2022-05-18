import socket, time, os, sys, tqdm
from datetime import datetime

HOST = "localhost"
PORT = 5001
FILENAME = sys.argv[1]
FILESIZE = os.path.getsize(FILENAME) 
BUFFER = int(sys.argv[2])

def client_udp():
    try:
        blocks = 0
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #sock.sendto(FILENAME.encode(), (UDP_IP, UDP_PORT))
        sock.sendto(f"{FILENAME}</>{FILESIZE}".encode(), (HOST, PORT))
        #print(file_name)

        f = open(FILENAME, "rb")
        data = f.read(BUFFER)

        progress_bar = tqdm.tqdm(range(FILESIZE), f"Sending {FILENAME}", unit="B", unit_scale=True, unit_divisor=1024)
        while(data):
            #blocks2 = blocks2 + 1
            if(sock.sendto(data, (HOST, PORT))):
                data = f.read(BUFFER)
                progress_bar.update(len(data))
                blocks = blocks + 1
                #time.sleep(0.02) # Give receiver a bit time to save
    finally:
        sock.close()
        f.close()
        return blocks

if __name__ == "__main__":
    tstart = datetime.now()
    print(f"BLOCKS GENERATED: {client_udp()}")
    tend = datetime.now()
    print (f"TIME ELAPSED: {(tend - tstart).total_seconds()*1000}")
