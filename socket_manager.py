# socket_manager.py

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
    return sock.recv(2048)

def close_socket(sock):
    """Close the socket."""
    sock.close()
