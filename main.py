import socket
import threading

PORTAS = [21, 22, 80, 443]

def escutar_porta(porta):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("0.0.0.0", porta))  
        server_socket.listen(5)

        print(f"[*] Monitorando conexões na porta {porta}...")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"[!] Conexão detectada na porta {porta} de {addr[0]}")

            try:
                dados = client_socket.recv(1024).decode(errors="ignore")  entrada do 
                if dados:
                    print(f"[+] Dados recebidos de {addr[0]} na porta {porta}: {dados.strip()}")
            except Exception as e:
                print(f"[X] Erro ao capturar dados: {e}")

            client_socket.close()
    except Exception as e:
        print(f"[X] Erro na porta {porta}: {e}")

for porta in PORTAS:
    threading.Thread(target=escutar_porta, args=(porta,), daemon=True).start()

# Mantém o script rodando
while True:
    pass
