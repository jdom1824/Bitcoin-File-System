# handle_pong.py

import struct
import time
import hashlib
from utils import send_message

def handle_pong(payload):
    """Maneja la respuesta pong y calcula la latencia."""
    if len(payload) < 8:
        return "Error: Incomplete payload for pong."
    
    # Extrae el nonce del pong, que es el timestamp del ping
    received_nonce = struct.unpack('<Q', payload[:8])[0]
    
    # Obtén el timestamp actual en milisegundos
    current_time = int(time.time() * 1000)
    
    # Calcula la latencia en segundos
    latency = (current_time - received_nonce) / 1000
    
    # Imprime la latencia
    print(f"Pong received, latency: {latency:.3f} seconds")
    
    # Devuelve un diccionario con la información de la respuesta
    return {
        'type': 'pong',
        'nonce': received_nonce,
        'latency': latency
    }

def send_pong(sock, nonce):
    """Envía un mensaje pong con el mismo nonce recibido en el ping."""
    command = b'pong\x00\x00\x00\x00\x00\x00\x00'
    
    # Crea el payload con el nonce
    payload = struct.pack('<Q', nonce)
    
    # Calcula la longitud del payload
    length = struct.pack('<I', len(payload))
    
    # Calcula el checksum del payload
    checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    
    # Construye el mensaje final
    message = b'\xf9\xbe\xb4\xd9' + command + length + checksum + payload
    
    # Imprime un mensaje indicando que se ha enviado el pong
    print("send pong")
    
    # Envía el mensaje 
    send_message(sock, message)
