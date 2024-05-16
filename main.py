# main.py
import threading
import time
from socket_manager import ConnectionManager

def main():
    """Función principal que maneja la conexión y comunicación con un nodo de Bitcoin."""
    # Detalles del nodo Bitcoin al que te quieres conectar
    node_ip = '188.174.58.144'  # Cambia esto por la IP real del nodo
    node_port = 8333  # Puerto estándar de Bitcoin

    manager = ConnectionManager(node_ip, node_port)
    manager_thread = threading.Thread(target=manager.manage_connection)
    manager_thread.daemon = True
    manager_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down.")

if __name__ == "__main__":
    main()
