# main.py
import threading
import time
from socket_manager import create_socket, send_message, receive_message, close_socket
from version_message import create_version_message
from verack_message import create_verack_message
from decode_version_message import decode_version_message
from decode_ping_inv_data import decode_message_ping_inv
from ping import send_ping

def send_periodic_ping(sock):
    try:
        time.sleep(30) # 5 mins to next ping
        while True:
            send_ping(sock)
            print("Sent ping message.")
            time.sleep(30)  # Esperar 60 segundos antes de enviar el próximo ping
    except Exception as e:
        print("An error occurred in ping thread:", e)

def main():
    # Detalles del nodo Bitcoin al que te quieres conectar
    node_ip = '84.151.31.7'  # Cambia esto por la IP real del nodo
    node_port = 8333  # Puerto estándar de Bitcoin

    # Crear y conectar el socket
    sock = create_socket(node_ip, node_port)

    # Crear y enviar el mensaje de versión
    version_msg = create_version_message()
    send_message(sock, version_msg)
    print("Sent version message.")

    # Esperar y recibir el mensaje de versión del nodo remoto
    response = receive_message(sock)
    response_message = decode_version_message(response)
    print(response_message)

    # Enviar el mensaje verack en respuesta al mensaje de versión recibido
    verack_msg = create_verack_message()
    send_message(sock, verack_msg)
    print("Sent verack message.")

    # Iniciar el hilo para enviar pings periódicos
    ping_thread = threading.Thread(target=send_periodic_ping, args=(sock,))
    ping_thread.daemon = True
    ping_thread.start()

    try:
        while True:
            response = receive_message(sock)  # Asegurarse de pasar sock aquí
            if not response:
                print("No more data received. Connection may be closed.")
                break
            # Procesar el mensaje recibido
            decode_message_ping_inv(response)
            
            # Aquí añadirías lógica para decodificar y responder a diferentes tipos de mensajes
    except Exception as e:
        print("An error occurred:", e)
    finally:
        close_socket(sock)

if __name__ == "__main__":
    main()
