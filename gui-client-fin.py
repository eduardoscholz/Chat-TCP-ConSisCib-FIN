import tkinter as tk
from tkinter import scrolledtext
import socket
import threading

host, port = '255.255.255.255', 65535
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def abrir_chat():
    global nickname
    nickname = entrada_nome.get()
    client.connect((host, port))
    client.send(nickname.encode('UTF-8'))

    janela_inicial.destroy()

    chat_thread = threading.Thread(target = criar_janela_chat)
    chat_thread.start()

def criar_janela_chat():
    global entrada_mensagem, area_chat, root

    root = tk.Tk()
    root.title(f"Canal TCP em {host}")
    root.geometry("400x500")
    root.config(bg="grey")

    #pack chat
    area_chat = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, font=("Helvetica", 12))
    area_chat.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    area_chat.config(bg="black", fg="white", cursor="arrow")

    #frame chat
    frame_inferior = tk.Frame(root)
    frame_inferior.pack(padx=10, pady=10, fill=tk.X)
    frame_inferior.config(bg="grey")

    #entry message
    entrada_mensagem = tk.Entry(frame_inferior, font=("Helvetica", 12))
    entrada_mensagem.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
    entrada_mensagem.config(bg="black", fg="white")

    #button send
    botao_enviar = tk.Button(frame_inferior, text="Enviar", command=write, font=("Helvetica", 12))
    botao_enviar.pack(side=tk.RIGHT)
    botao_enviar.config(bg="black", fg="white", cursor="hand2")

    receive_thread = threading.Thread(target = receive)
    receive_thread.start()

    write_thread = threading.Thread(target = write)
    write_thread.start()

    root.mainloop()

def receive():
    while True:
        try:
            mensagem = client.recv(1024).decode('UTF-8')
            if mensagem == 'NICK':
                client.send(nickname.encode('UTF-8'))
            else:
                area_chat.config(state=tk.NORMAL)
                area_chat.insert(tk.END, f"{mensagem}\n")
                area_chat.config(state=tk.DISABLED)
                area_chat.yview(tk.END)
        except:
            print('Você foi desconectado.')
            client.close()
            root.destroy()
            break

def write():
    mensagem = entrada_mensagem.get()
    if mensagem.strip():
        if mensagem.startswith('/pm'):
            client.send(mensagem.encode('UTF-8'))
            entrada_mensagem.delete(0, tk.END)

        elif mensagem.startswith('/quit'):
            client.close()
            root.destroy()
        else:
            mensagem = f"{nickname}: {entrada_mensagem.get()}"
            client.send(mensagem.encode('UTF-8'))
            area_chat.yview(tk.END)
            entrada_mensagem.delete(0, tk.END)

#window nickname
janela_inicial = tk.Tk()
janela_inicial.title("login")
janela_inicial.geometry("300x150")

#label nickname screen
label_instrucoes = tk.Label(janela_inicial, text="Insira seu nome para entrar no chat:", font=("Arial", 12))
label_instrucoes.pack(pady=10)

#nickname entry
entrada_nome = tk.Entry(janela_inicial, font=("Arial", 12))
entrada_nome.pack(pady=5)

#label warning
aviso_label = tk.Label(janela_inicial, text="", font=("Arial", 10), fg="red")
aviso_label.pack()

#button confirm name
botao_confirmar = tk.Button(janela_inicial, text="Entrar", command=abrir_chat, font=("Arial", 12))
botao_confirmar.pack(pady=10)

janela_inicial.mainloop()