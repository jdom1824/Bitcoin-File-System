# utils.py
import socket

def create_socket(ip, port):
    """Create a TCP socket and connect to the specified IP and port."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    return s

def send_message(sock, message):
    """Send a message through the socket."""
    sock.sendall(message)

def receive_message(sock):
    """Receive a message from the socket."""
    try:
        return sock.recv(2048)
    except socket.error as e:
        print(f"Socket error: {e}")
        return None

def close_socket(sock):
    """Close the socket."""
    try:
        sock.close()
    except Exception as e:
        print(f"Error closing socket: {e}")
