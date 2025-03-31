import socket

send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

ip = input("请输入对方ip:")
port = int(input("请输入对方port:"))
send_data = input("请输入你要发送的消息：")
send_socket.sendto(send_data.encode("utf-8"), (ip, port))

send_socket.close()

