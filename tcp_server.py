from fileinput import filename
import socket, tqdm, os, sys
from datetime import datetime
# device's IP address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5001
BUFFER = int(sys.argv[1])

def server_tcp():
    try:
        #blocks = 0
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((SERVER_HOST, SERVER_PORT))

        server_socket.listen(5)
        print(f"Listening as {SERVER_HOST}:{SERVER_PORT}")

        # aceita conexão, caso haja uma
        client_socket, address = server_socket.accept() 
        
        # printa o endereço conectado
        print(f"{address} is connected.")

        # recebe as informações dos dados, utilizando socket do cliente
        received = client_socket.recv(BUFFER).decode()
        filename, filesize = received.split("</>")
        
        # remove caminho absoluto
        filename = os.path.basename(filename) 
    
        # casting para inteiro
        filesize = int(filesize)  

        # recebe arquivo do socket 
        progress_bar = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "wb") as f:
            while True:
                data = client_socket.recv(BUFFER)
                if not data:    
                    #se nada for recebido, a transmissão termina
                    break
                f.write(data)
                # update the progress bar
                progress_bar.update(len(data))
                #blocks = blocks + 1

    finally:
        # fecha o socket do cliente
        client_socket.close()
        # fecha o socket do server
        server_socket.close()

        return

if __name__ == "__main__":
    #TSTART = datetime.now()
    server_tcp()
