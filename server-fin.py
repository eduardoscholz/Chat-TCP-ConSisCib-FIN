import threading
import socket

host = "255.255.255.255"
port = 65535

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024).decode('UTF-8')

            if message.startswith('/pm'):
                parts = message.split(' ', 2)
                if len(parts) >= 3:
                    target_nickname = parts[1]
                    private_message = parts[2]
                    if target_nickname in nicknames:
                        target_index = nicknames.index(target_nickname)
                        target_client = clients[target_index]
                        
                        sender_index = clients.index(client)
                        sender_nickname = nicknames[sender_index]
                        
                        private_msg_to_sender = f'você para {target_nickname}: {private_message}'.encode('UTF-8')
                        private_msg_to_target = f'{sender_nickname} para você: {private_message}'.encode('UTF-8')
                        
                        client.send(private_msg_to_sender)
                        target_client.send(private_msg_to_target)
                    else:
                        client.send('usuário não encontrado'.encode('UTF-8'))
                else:
                    client.send('formato inválido. /pm <destinatário> <mensagem>'.encode('UTF-8'))
            else:
                broadcast(message.encode('UTF-8'))
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} saiu do canal.'.encode('UTF-8'))
            nicknames.remove(nickname)
            break



def receive():
    while True:
        client, address = server.accept()
        print(f'{str(address)} conectado')

        client.send('NICK'.encode('UTF-8'))
        nickname = client.recv(1024).decode('UTF-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f'nick do client: {nickname}')
        broadcast(f'{nickname} entrou no canal.'.encode('UTF-8'))

        thread = threading.Thread(target = handle, args = (client,))
        thread.start()

print(f'canal aberto no ip: {host}')
receive()
