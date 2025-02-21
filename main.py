from scapy.all import sniff, TCP

conexoes_ssh = set()  # Para rastrear conexões SSH

def monitorar_pacotes(pacote):
    if pacote.haslayer('IP') and pacote.haslayer(TCP):
        ip_src = pacote['IP'].src
        ip_dst = pacote['IP'].dst
        porta_src = pacote.sport
        porta_dst = pacote.dport
        
        if porta_dst == 22:  # Verifica se a porta de destino é 22 (SSH)
            if pacote[TCP].flags == 'S':  # Pacote SYN
                print(f"[!] Tentativa de acesso SSH detectada: {ip_src}:{porta_src} -> {ip_dst}:{porta_dst}")
            elif pacote[TCP].flags == 'SA':  # Pacote SYN-ACK
                conexao = (ip_src, porta_src, ip_dst, porta_dst)
                if conexao not in conexoes_ssh:
                    conexoes_ssh.add(conexao)
                    print(f"[+] Conexão SSH estabelecida: {ip_src}:{porta_src} -> {ip_dst}:{porta_dst}")
            elif pacote[TCP].flags == 'A':  # Pacote ACK
                if (ip_dst, porta_dst, ip_src, porta_src) in conexoes_ssh:
                    print(f"[+] Acesso SSH confirmado: {ip_src}:{porta_src} -> {ip_dst}:{porta_dst}")
                else:
                    print(f"[!] Acesso SSH não registrado: {ip_src}:{porta_src} -> {ip_dst}:{porta_dst}")

# Defina a porta que você deseja monitorar
PORTA_MONITORADA = [22]

# Filtra pacotes para a porta SSH
filtro = f"tcp and (port {' or port '.join(map(str, PORTA_MONITORADA))})"

# Inicia a captura de pacotes
sniff(filter=filtro, prn=monitorar_pacotes, store=0, iface='nome_da_interface')  # Substitua 'nome_da_interface' pela interface correta
