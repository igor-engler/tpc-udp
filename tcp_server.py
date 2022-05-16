import socket
import tqdm
import os
# device's IP address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5001
BUFFER = 4096 # recebe 4096 bytes por vez (mudar pra receber como comando)
SEPARATOR = "</>"


if __name__ == "__main__":
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind((SERVER_HOST, SERVER_PORT))

    s.listen(5)
    print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

    # aceita conexão, caso haja uma
    client_socket, address = s.accept() 
    
    # printa o endereço conectado
    print(f"[+] {address} is connected.")

    # recebe as informações dos dados, utilizando socket do cliente
    received = client_socket.recv(BUFFER).decode()
    filename, filesize = received.split(SEPARATOR)
    
    # remove caminho absoluto
    filename = os.path.basename(filename) 
   
    # casting para inteiro
    filesize = int(filesize)  

    # recebe arquivo do socket 
    progress_bar = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=BUFFER)
    with open(filename, "wb") as f:
        while True:
            data = client_socket.recv(BUFFER)
            if not data:    
                #se nada for recebido, a transmissão termina
                break
            f.write(data)
            # update the progress bar
            progress_bar.update(len(data))

    # fecha o socket do cliente
    client_socket.close()
    # fecha o socket do server
    s.close()
