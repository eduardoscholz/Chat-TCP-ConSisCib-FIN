import socket
import threading

host = '255.255.255.255' #input('ip: ')
port = 65535 #int(input('port: '))

nickname = input('Nickname: ')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('UTF-8')
            if message == 'NICK':
                client.send(nickname.encode('UTF-8'))
            else:
                print(message)
        except:
            print('Você foi desconectado.')
            client.close()
            break

def write():
    while True:
        message = input('')
        if message.startswith('/pm'):
            client.send(message.encode('UTF-8'))

        elif message.startswith('/quit'):
            client.close()
            break
        else:
            message = f'{nickname}: {message}'
            client.send(message.encode('UTF-8'))


receive_thread = threading.Thread(target = receive)
receive_thread.start()

write_thread = threading.Thread(target = write)
write_thread.start()