# decode_inv_data.py

import struct

def decode_varint(data):
    """Decodifica un número VarInt de Bitcoin."""
    first_byte = data[0]
    if first_byte < 0xfd:
        return first_byte, 1
    if first_byte == 0xfd:
        return struct.unpack('<H', data[1:3])[0], 3
    if first_byte == 0xfe:
        return struct.unpack('<I', data[1:5])[0], 5
    if first_byte == 0xff:
        return struct.unpack('<Q', data[1:9])[0], 9

def decode_inv(data):
    """Decodifica un mensaje inv de Bitcoin."""
    if len(data) < 24:
        return "Error: Incomplete message header."
    
    magic, command, length, checksum = struct.unpack('<4s12sI4s', data[:24])
    command = command.strip(b'\x00').decode()
    
    if command != "inv":
        return None, "Not an inv message"
    
    payload = data[24:24+length]
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
            inv_hash = bytes.fromhex(item['hash'])  # Convertir de hex a bytes y revertir el endianness
            inv_hash = inv_hash[::-1].hex()
            print(f"Transaction {inv_hash} received")
            return {'type': 'inv', 'items': [item]}, None
        elif item['type'] == 2:  # MSG_BLOCK
            inv_hash = bytes.fromhex(item['hash'])  # Convertir de hex a bytes y revertir el endianness
            inv_hash = inv_hash[::-1].hex()
            print(f"Block {inv_hash} received")
            return {'type': 'inv', 'items': [item]}, None
        elif item['type'] == 3:  # MSG_FILTERED_BLOCK
            print(f"Filtered Block {item['hash']} received")
            return {'type': 'inv', 'items': [item]}, None
        elif item['type'] == 4:  # MSG_CMPCT_BLOCK
            print(f"Compact Block {item['hash']} received")
            return {'type': 'inv', 'items': [item]}, None
        elif item['type'] == 5:  # MSG_WITNESS_TX
            inv_hash = bytes.fromhex(item['hash'])  # Convertir de hex a bytes y revertir el endianness
            inv_hash = inv_hash[::-1].hex()
            print(f"Witness Transaction {inv_hash} received")
            return {'type': 'inv', 'items': [item]}, None
        elif item['type'] == 6:  # MSG_WITNESS_BLOCK
            inv_hash = bytes.fromhex(item['hash'])  # Convertir de hex a bytes y revertir el endianness
            inv_hash = inv_hash[::-1].hex()
            print(f"Witness Block {inv_hash} received")
            return {'type': 'inv', 'items': [item]}, None
        elif item['type'] == 7:  # MSG_FILTERED_WITNESS_BLOCK
            print(f"Filtered Witness Block {item['hash']} received")
            return {'type': 'inv', 'items': [item]}, None
        else:
            print(f"Unknown type {item['type']} received")
            return {'type': 'inv', 'items': [item]}, None

    return None, None
    
    
