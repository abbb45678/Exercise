import socket

recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

ip = input("请输入你的ip:")
port = int(input("请输入你的port:"))
recv_socket.bind((ip, port))

recv_data = recv_socket.recvfrom(1024)

print(f"{recv_data[1][0]}:{recv_data[0].decode('utf-8')}")

recv_socket.close()
