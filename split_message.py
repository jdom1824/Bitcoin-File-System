# split_message.py

import struct
from verack_message import decode_verack
from decode_ping_inv_data import decode_message_ping_inv

def process_message(sock, message):
    results = []
    try:
        # Separar mensajes en el buffer recibido
        while len(message) >= 24:
            magic = message[:4]
            if magic != b'\xf9\xbe\xb4\xd9':
                print("Error: Incorrect magic bytes.")
                return
            
            # Obtener tamaño del payload
            length = struct.unpack('<I', message[16:20])[0]
            total_length = 24 + length
            
            # Verificar si tenemos el mensaje completo
            if len(message) < total_length:
                print("Error: Incomplete message.")
                return
            
            # Extraer y procesar el mensaje completo
            single_message = message[:total_length]
            message = message[total_length:]

            # Decodificar el mensaje
            command = single_message[4:16].strip(b'\x00').decode()
            if command == 'verack':
                result = decode_verack(single_message)
                results.append(result)
            else:
                result = decode_message_ping_inv(sock, single_message)
                results.append(result)
    except Exception as e:
        print(f"Error processing message: {e}")
    return results
