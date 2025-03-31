import socket
import threading


def send_data(udp_socket):
    ip = input("请输入对方ip:")
    port = int(input("请输入对方port:"))
    print("退出该聊天按a！")
    while True:
        send_mas = input("请输入你要发送的消息：")
        if send_mas == "a":
            break
        else:
            udp_socket.sendto(send_mas.encode("utf-8"), (ip, port))


def recv_data(udp_socket):
    while True:  # 持续监听
        try:
            recv_mas = udp_socket.recvfrom(1024)
            print(f"\n来自({recv_mas[1][0]}:{recv_mas[1][1]})的消息: {recv_mas[0].decode('utf-8')}")
        except OSError as e:  # 捕获套接字关闭的异常
            if udp_socket._closed:  # 确认套接字已关闭
                print("接收线程已安全退出。")
                break
            else:
                print(f"接收错误: {e}")
        except Exception as e:  # 其他异常处理
            print(f"未知错误: {e}")


def login():
    print("——————————————登录账号——————————————")
    users = {}
    with open("users.txt", "r", encoding="utf-8") as f:
        for line in f:
            mas = line.strip().split(',')
            username, password = mas
            users[username] = password
    your_name = input("请输入你的用户名：")
    your_password = input("请输入你的密码：")
    if users[your_name] == your_password:
        print("登陆成功！")
        print("——————————————登录成功——————————————")
        main()
    else:
        print("用户名或密码输入错误！")
        print("1.重新输入")
        print("2.没有账号，返回注册")
        print("3.退出系统")
        n = input("请输入你的操作选项")
        while True:
            if n == "1":
                login()
            elif n == "2":
                register()
            elif n == "3":
                print("正在退出...")
                break
            else:
                print("请输入有效选项！")


def register():
    print("——————————————注册账号——————————————")
    new_name = input("请输入你的用户名：")
    new_password = input("请输入你的密码：")
    user_info = f"{new_name},{new_password}\n"
    password = input("请确认密码：")
    if password == new_password:
        with open("users.txt", "a", encoding="utf-8") as f:
            f.write(user_info)

        print("--------------------")
        print("注册成功！！")
        print("1.返回登录")
        print("2.退出系统")
        print("--------------------")

        n = input("请输入你的操作选项：")
        while True:
            if n == "1":
                login()
            elif n == "2":
                print("正在退出...")
                break
    else:
        print("密码不一致，注册失败！")

        print("--------------------")
        print("1.重新注册")
        print("2.退出系统")
        print("--------------------")

        n = input("请输入你的操作选项：")
        while True:
            if n == "1":
                register()
            elif n == "2":
                print("正在退出...")
                break
    print("——————————————注册账号——————————————")
    # login_menu()


def login_menu():
    print("--------------------")
    print("a.登录")
    print("b.注册")
    print("c.退出")
    print("--------------------")

    choice = input("请输入你的选项：")
    if choice == "a":
        login()
    elif choice == "b":
        register()
    elif choice == "c":
        exit()
    else:
        print("输入错误！！")


def main():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip = input("请输入你的ip:")
    port = int(input("请输入你的port:"))
    udp_socket.bind((ip, port))

    recv_thread = threading.Thread(target=recv_data, args=(udp_socket,))
    recv_thread.daemon = True
    recv_thread.start()

    print("——————————————聊天界面——————————————")
    print("1.发消息")
    print("2.退出")
    while True:
        print()
        choice = input("请输入你的选项：")
        if choice == "1":
            send_data(udp_socket)
        elif choice == "2":
            udp_socket.close()
            exit()
        else:
            print("请输入有效选项！！")


login_menu()
