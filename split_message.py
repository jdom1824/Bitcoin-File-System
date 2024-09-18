# split_message.py
import struct

incomplete_message = b''

def process_message(message):
    global incomplete_message
    results = []
    message = incomplete_message + message
    try:
        while len(message) >= 24:
            magic = message[:4]
            if magic != b'\xf9\xbe\xb4\xd9':
                print("Error: Incorrect magic bytes.")
                return results
            
            # Obtener tamaño del payload
            length = struct.unpack('<I', message[16:20])[0]
            total_length = 24 + length
            
            # Verificar si tenemos el mensaje completo
            if len(message) < total_length:
                incomplete_message = message  # Guardar el mensaje incompleto
                return results
            
            # Extraer y procesar el mensaje completo
            single_message = message[:total_length]
            message = message[total_length:]

            # Decodificar el comando
            command = single_message[4:16].strip(b'\x00').decode('ascii')
            
            result = {"type": command, "message": single_message}
            results.append(result)
   
        incomplete_message = b''  # Clear incomplete message buffer after processing all complete messages
    except Exception as e:
        print(f"Error processing message: {e}")
    return results
