# decode_ping_inv_data.py

import struct
from socket_manager import send_message
import hashlib  # Asegúrate de que esta línea esté incluida
import time

def handle_pong(payload):
    """ Maneja la respuesta pong y calcula la latencia."""
    if len(payload) < 8:
        return "Error: Incomplete payload for pong."
    received_nonce = struct.unpack('<Q', payload[:8])[0]  # Extrae el nonce del pong, que es el timestamp del ping
    current_time = int(time.time() * 1000)  # Obtén el timestamp actual en milisegundos
    latency = (current_time - received_nonce) / 1000  # Calcula la latencia en segundos
    print(f"Pong received, latency: {latency:.3f} seconds")
    return {'type': 'pong', 'nonce': received_nonce, 'latency': latency}


def decode_varint(data):
    """ Decodifica un número VarInt de Bitcoin. """
    first_byte = data[0]
    if first_byte < 0xfd:
        return first_byte, 1
    if first_byte == 0xfd:
        return struct.unpack('<H', data[1:3])[0], 3
    if first_byte == 0xfe:
        return struct.unpack('<I', data[1:5])[0], 5
    if first_byte == 0xff:
        return struct.unpack('<Q', data[1:9])[0], 9

def decode_inventory_item(data):
    inv_type, inv_hash = struct.unpack('<I32s', data)
    return {'type': inv_type, 'hash': inv_hash.hex()}

def decode_message_ping_inv(data):
    if len(data) < 24:
        return "Error: Incomplete message header."
    
    magic, command, length, checksum = struct.unpack('<4s12sI4s', data[:24])
    command = command.strip(b'\x00').decode()
    payload = data[24:24+length]
    
    if command == "ping":
        if len(payload) < 8:
            return "Error: Incomplete payload for ping."
        nonce = struct.unpack('<Q', payload[:8])[0]
        send_pong(nonce)  # Enviar pong automáticamente
        return {'type': 'ping', 'nonce': nonce}
    
    elif command == "pong":
            return handle_pong(payload)
    
    elif command == "inv":
        count, offset = decode_varint(payload)
        items = []
        current = offset
        while current < len(payload) and len(items) < count:
            if current + 36 > len(payload):
                break
            inv_type, inv_hash = struct.unpack_from('<I32s', payload, current)
            items.append({'type': inv_type, 'hash': inv_hash.hex()})
            current += 36
        
        for item in items:
            if item['type'] == 1:  # MSG_TX
                continue
            elif item['type'] == 2:  # MSG_BLOCK
                inv_hash = bytes.fromhex(item['hash'])  ##Como estan en little-endian invierto
                inv_hash = inv_hash[::-1].hex()
                print(f"Block {inv_hash} received")
                time.sleep(60)  # Espera un minuto
                send_ping()  # Envía un ping
            elif item['type'] == 3:  # MSG_FILTERED_BLOCK
                print(f"Filtered Block {item['hash']} received")
            elif item['type'] == 4:  # MSG_CMPCT_BLOCK
                print(f"Compact Block {item['hash']} received")
        
        return {'type': 'inv', 'items': items}
    
    return "Unhandled or ignored message type"

def send_pong(nonce):
    """Envía un mensaje pong con el mismo nonce recibido en el ping."""
    command = b'pong\x00\x00\x00\x00\x00\x00\x00'
    payload = struct.pack('<Q', nonce)
    length = struct.pack('<I', len(payload))
    checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    message = b'\xf9\xbe\xb4\xd9' + command + length + checksum + payload
    send_message(message)


def send_ping():
    """Envía un mensaje ping con un nonce generado aleatoriamente."""
    nonce = struct.unpack('<Q', struct.pack('<Q', int(time.time()*1000)))[0]  # Usa el timestamp como nonce
    command = b'ping\x00\x00\x00\x00\x00\x00\x00'
    payload = struct.pack('<Q', nonce)
    length = struct.pack('<I', len(payload))
    checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    message = b'\xf9\xbe\xb4\xd9' + command + length + checksum + payload
    send_message(message)