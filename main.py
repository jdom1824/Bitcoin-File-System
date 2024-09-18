import threading
import time
from socket_manager import ConnectionManager
from listener import listen_for_messages

def main():
    node_ip = '190.145.127.254'  # Cambia esto por la IP real del nodo
    node_port = 8333  # Puerto estándar de Bitcoin

    while True:
        manager = ConnectionManager(node_ip, node_port)
        sock = manager.connect_to_node()
        if sock:
            print("Handshake successful")
            listener_thread = threading.Thread(target=listen_for_messages, args=(manager.sock, node_ip))
            listener_thread.daemon = True
            listener_thread.start()
            listener_thread.join() 
        else:
            print("Handshake failed. Retrying in 1 minute...")
            for i in range(60, 0, -1):
                print(f"Retrying in {i} seconds...", end="\r")
                time.sleep(1)

if __name__ == "__main__":
    main()
