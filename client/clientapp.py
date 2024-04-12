import Pyro4
import socket
import _thread as thread
import threading
import sys

uri = input("Masukkan Pyro URI server : ").strip()

server = Pyro4.Proxy(uri)        

tcp_port = udp_port = 1234
condition = False

def tcp_listen(sock, server):
    while True:
        conn, addr = sock.accept()
        try:
            while True:
                data = conn.recv(1024)
                last_msg = server.get()
                if len(data) == 0:
                    break
                print("recv:", data)
                msg = server.send(addr,data.decode('utf-8'))
                if last_msg:
                    conn.sendall(bytes(last_msg["msg"], 'utf-8'))
                else:
                    conn.sendall(data)
        except Exception:
            pass
        except KeyboardInterrupt:
            pass
        try:
            conn.close()
        except Exception:
            pass
        except KeyboardInterrupt:
            pass

def udp_listen(conn, server):
    try:
        while True:
            data, addr = conn.recvfrom(1024)
            last_msg = server.get()
            if len(data) != 0:
                msg = server.send(addr,data.decode('utf-8'))
                if last_msg:
                    conn.sendto(bytes(last_msg["msg"], 'utf-8'),addr)
                else:
                    conn.sendto(data,addr)
    except KeyboardInterrupt:
        sys.exit()

sockTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # UDP

server_addressTCP = ('localhost', tcp_port)
server_addressUDP = ('localhost', udp_port)

sockTCP.bind(server_addressTCP)
sockUDP.bind(server_addressUDP)

sockTCP.listen(20)

t1 = threading.Thread(target=tcp_listen, args=(sockTCP, server,))
t2 = threading.Thread(target=udp_listen, args=(sockUDP, server,))

print("Waiting for connections ...")

t1.start()
t2.start()

t1.join()
t2.join()