import socket
import ssl

ip = '192.168.0.153'

def main():
    # Configuração do servidor
    server_cert = "certs/certificate.pem"
    server_key = "keys/key_certificate.pem"
    
    # Criar o socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, 8443))  # IP da máquina e porta 8443
    server_socket.listen(5)

    # Wrapping com TLS
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=server_cert, keyfile=server_key)
    context.verify_mode = ssl.CERT_REQUIRED

    print("Servidor pronto para aceitar conexões TLS...")
    while True:
        conn, addr = server_socket.accept()
        with context.wrap_socket(conn, server_side=True) as tls_conn:
            print(f"Conexão estabelecida com {addr}")
            data = tls_conn.recv(1024).decode()
            print(f"Recebido: {data}")
            tls_conn.send(b"Resposta segura do servidor")
            print("Conexão encerrada.\n")

if __name__ == "__main__":
    main()
