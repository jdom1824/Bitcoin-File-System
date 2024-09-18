#get_block_hash.py

import struct
import hashlib
'''
getblockhash Message:
┌─────────────┬──────────────┬───────────────┬───────┬─────────────────────────────────────┐
│ Name        │ Example Data │ Format        │ Size  │ Example Bytes                       │
├─────────────┼──────────────┼───────────────┼───────┼─────────────────────────────────────┤
│ Magic Bytes │              │ bytes         │     4 │ F9 BE B4 D9                         │
│ Command     │ "getblockhash" │ ascii bytes │    12 │ 67 65 74 62 6C 6F 63 6B 68 61 73 68 │
│ Payload Size│ 4            │ little-endian │     4 │ 04 00 00 00                         │
│ Checksum    │              │ bytes         │     4 │ D9 E3 D7 6A                         │
│ Payload     │ Block Height │ little-endian │     4 │ 80 41 0A 00                         │
└─────────────┴──────────────┴───────────────┴───────┴─────────────────────────────────────┘
'''

def build_message(command, payload):
    magic = b'\xf9\xbe\xb4\xd9'  # Magic number for mainnet
    command = command.ljust(12, b'\x00')  # Command + padding to ensure it's 12 bytes
    payload_size = struct.pack('<I', len(payload))  # Payload size in little-endian format
    checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]  # First 4 bytes of double SHA-256 checksum
    message = magic + command + payload_size + checksum + payload  # Concatenate all parts to form the final message
    return message

def build_getdata_payload(block_hash):
    inv_type = 2  # MSG_BLOCK = 2
    count = 1
    compact_count = struct.pack('<B', count)  # Using <B (unsigned char) for simplicity
    block_hash_bytes = bytes.fromhex(block_hash)[::-1]  # Convert hash to little-endian
    payload = compact_count + struct.pack('<I', inv_type) + block_hash_bytes
    return payload

def request_block_data(sock, block_hash):
    payload = build_getdata_payload(block_hash)
    message = build_message(b'getdata', payload)
    sock.sendall(message)

def save_block_to_file(block_data, file_path):
    with open(file_path, 'wb') as file:
        file.write(block_data)
    print(f"Block stored in {file_path}")
