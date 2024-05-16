# socket_manager.py
import time
import threading
from utils import create_socket, send_message, receive_message, close_socket
from version_message import create_version_message
from verack_message import create_verack_message
from decode_version_message import decode_version_message
from decode_ping_inv_data import decode_message_ping_inv
from ping import send_ping

class ConnectionManager:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sock = None
        self.lock = threading.Lock()
        self.thread = None

    def connect_to_node(self):
        try:
            sock = create_socket(self.ip, self.port)
            self.lock.acquire()
            self.sock = sock
            self.lock.release()

            # Enviar y recibir mensajes de versión y verack
            version_msg = create_version_message()
            send_message(sock, version_msg)
            print(f"Sent version message to {self.ip}")

            response = receive_message(sock)
            if response:
                response_message = decode_version_message(response)
                print(response_message)

                verack_msg = create_verack_message()
                send_message(sock, verack_msg)
                print(f"Sent verack message to {self.ip}")

                # Iniciar hilo para enviar pings periódicos
                self.thread = threading.Thread(target=self.send_periodic_ping)
                self.thread.daemon = True
                self.thread.start()
                return sock
            else:
                print(f"No version response from {self.ip}. Closing socket.")
                self.reconnect()
                return None
        except Exception as e:
            print(f"Failed to connect to {self.ip}: {e}")
            return None

    def send_periodic_ping(self):
        try:
            time.sleep(120)  # Esperar 120 segundos antes de enviar el primer ping
            while True:
                try:
                    send_ping(self.sock)
                    print(f"Sent ping message to {self.ip}.")
                    time.sleep(120)  # Esperar 120 segundos antes de enviar el próximo ping
                except Exception as e:
                    print(f"Error sending ping to {self.ip}: {e}")
                    self.reconnect()
                    break
        except Exception as e:
            print(f"An error occurred in ping thread for {self.ip}: {e}")

    def manage_connection(self):
        self.connect_to_node()

        while True:
            try:
                response = receive_message(self.sock)
                if not response:
                    print("No more data received. Connection may be closed.")
                    # Intentar enviar un ping antes de reconectar
                    try:
                        send_ping(self.sock)
                        print(f"Sent ping message to {self.ip} after no data received.")
                        response = receive_message(self.sock)
                        if response:
                            self.process_message(response)
                            continue  # Si se recibe respuesta, continuar
                    except Exception as ping_error:
                        print(f"Ping failed after no data received: {ping_error}")
                    self.reconnect()
                else:
                    self.process_message(response)
            except Exception as e:
                print(f"Error with connection to {self.ip}: {e}")
                # Intentar enviar un ping antes de reconectar
                try:
                    send_ping(self.sock)
                    print(f"Sent ping message to {self.ip} after error.")
                    time.sleep(5)  # Esperar un momento para recibir respuesta
                    response = receive_message(self.sock)
                    if response:
                        self.process_message(response)
                        continue  # Si se recibe respuesta, continuar
                except Exception as ping_error:
                    print(f"Ping failed after error: {ping_error}")
                self.reconnect()
            time.sleep(5)

    def process_message(self, message):
        # Procesar el mensaje recibido
        # Decodificar y manejar diferentes tipos de mensajes aquí
        #print(f"Received message: {message}")
        decode_message_ping_inv(self.sock, message)
        # Añadir más lógica de procesamiento según sea necesario

    def reconnect(self):
        self.lock.acquire()
        if self.sock:
            close_socket(self.sock)
            self.sock = None
        self.lock.release()

        print(f"Reconnecting to {self.ip}")
        self.connect_to_node()