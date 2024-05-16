# ping.py
import struct
import time
import hashlib
from socket_manager import send_message

def create_ping_message():
    """Crea un mensaje ping con un nonce generado aleatoriamente."""
    nonce = struct.unpack('<Q', struct.pack('<Q', int(time.time() * 1000)))[0]  # Usa el timestamp como nonce
    command = b'ping' + b'\x00' * 8  # Command field debe ser 'ping' seguido de padding con ceros hasta completar 12 bytes
    payload = struct.pack('<Q', nonce)  # Nonce como payload
    length = struct.pack('<I', len(payload))  # Longitud del payload
    checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]  # Checksum de los primeros 4 bytes del hash doble SHA-256 del payload
    magic = b'\xf9\xbe\xb4\xd9'  # Magic number para mainnet
    message = magic + command + length + checksum + payload
    return message

def send_ping(sock):
    """Envía un mensaje ping a través del socket proporcionado."""
    ping_message = create_ping_message()
    send_message(sock, ping_message)
