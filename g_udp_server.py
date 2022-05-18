import socket, tqdm, select, os, sys
from datetime import datetime

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5001
TIMEOUT = 3
BUFFER =  int(sys.argv[1]) #500

def g_server_udp():
    blocks = 0
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))

    while True:
        data, address = server_socket.recvfrom(BUFFER)

        print(f"Waiting as {SERVER_HOST}:{SERVER_PORT}")

        print(f"{address} is connected.")
        if data:

            file_name, file_size = data.split(b"</>")
            file_name = os.path.basename(file_name) 

            f = open(file_name, 'wb')

            file_size = int(file_size)  
            
            progress_bar = tqdm.tqdm(range(file_size), f"Receiving {file_name}", unit="B", unit_scale=True, unit_divisor=1024)
            while True:
                ready = select.select([server_socket], [], [], TIMEOUT)
                if ready[0]:
                    data, address = server_socket.recvfrom(BUFFER)
                    f.write(data)
                    blocks = blocks + 1
                    server_socket.sendto(b"ack", address)
                    #sock.sendto("ACK".encode(), address)
                    
                else:
                    server_socket.sendto(b"nack", address)
                    f.close()
                    server_socket.close()
                    #TEND = datetime.now()
                    #print (TEND - TSTART)
                    return blocks
                progress_bar.update(len(data))
                

if __name__ == "__main__":
    #TSTART = datetime.now()
    print(f"BLOCKS RECEIVED: {g_server_udp()}")
    #TEND = datetime.now()
    #print (TEND - TSTART)
    