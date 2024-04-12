import socket

serverAddressPort   = ("localhost", 1234)
bufferSize          = 1024
end = False

# Create a UDP socket at client side
with socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) as s:
    while not end:
        msg = input("Masukkan Pesan [exit untuk berhenti]\n").strip()
        if msg != 'exit':
            # Send to server using created UDP socket
            s.sendto(str.encode(msg), serverAddressPort)

            msgFromServer = s.recvfrom(bufferSize)
            msg = msgFromServer[0].decode('utf-8')
            print(msg)
        else:
            end = True