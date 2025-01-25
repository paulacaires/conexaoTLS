import socket
import ssl

def main():
    # Configuração do cliente
    ip = '192.168.0.153'
    server_hostname = ip  # Trocar pelo IP do servidor
    server_port = 8443
    client_cert = "client_certs_keys/certificate.pem"
    client_key = "client_certs_keys/key.pem"

    # Criar o socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Wrapping com TLS
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_cert_chain(certfile=client_cert, keyfile=client_key)
    # context.load_verify_locations(cafile=server_cert)

    with context.wrap_socket(client_socket, server_hostname=server_hostname) as tls_socket:
        tls_socket.connect((server_hostname, server_port))
        tls_socket.send(b"Requisicao segura do cliente")
        response = tls_socket.recv(1024).decode()
        print(f"Resposta do servidor: {response}")

if __name__ == "__main__":
    main()
