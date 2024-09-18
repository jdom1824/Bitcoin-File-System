import threading
from utils import create_socket, send_message, receive_message, close_socket
from version_message import create_version_message
from split_message import process_message
from decode_version_message import decode_version_message
from decode_verack import decode_verack
from verack_message import create_verack_message

class ConnectionManager:
    
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sock = None
        self.lock = threading.Lock()

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

            # Recibir y procesar mensaje de versión
            response = receive_message(self.sock)
            if response:
                messages = process_message(response)
                version_received = False
                verack_received = False
                for message in messages:
                    print(f"Received message type: {message['type']}")
                    if message['type'] == 'version':
                        print(decode_version_message(message['message']))
                        version_received = True
                    if message['type'] == 'verack':
                        print(decode_verack(message['message']))
                        msg_verack = create_verack_message()
                        send_message(sock, msg_verack)
                        print("msg_verack_send")
                        verack_received = True
                if version_received and verack_received:
                    return self.sock
            return False
        except Exception as e:
            print(f"Failed to connect to {self.ip}: {e}")
            return False
        finally:
            if not (version_received and verack_received):
                close_socket(self.sock)
                print(f"Socket to {self.ip} closed.")