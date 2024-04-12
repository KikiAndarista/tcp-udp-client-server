import socket

HOST = "localhost" 
PORT = 1234 
end = False

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while not end:
        msg = input("Masukkan Pesan [exit untuk berhenti]\n").strip()
        if msg != 'exit':
            s.sendall(bytes(msg, 'utf-8'))
            data = s.recv(1024)
            print(data.decode('utf-8'))
        else:
            end = True
    s.close()
    

