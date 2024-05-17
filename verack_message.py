# verack_message
'''
Verack Message:
┌─────────────┬──────────────┬───────────────┬───────┬─────────────────────────────────────┐
│ Name        │ Example Data │ Format        │ Size  │ Example Bytes                       │
├─────────────┼──────────────┼───────────────┼───────┼─────────────────────────────────────┤
│ Magic Bytes │              │ bytes         │     4 │ F9 BE B4 D9                         │
│ Command     │ "verack"     │ ascii bytes   │    12 │ 76 65 72 61 63 6B 00 00 00 00 00 00 │
│ Size        │ 0            │ little-endian │     0 │ 00 00 00 00                         │
│ Checksum    │              │ bytes         │     4 │ 5D F6 E0 E2                         │
└─────────────┴──────────────┴───────────────┴───────┴─────────────────────────────────────┘
'''

import hashlib
import struct

def create_verack_message():
    magic = b'\xf9\xbe\xb4\xd9'  # Magic number for mainnet
    command = b'verack' + b'\x00' * (12 - len(b'verack'))  # Command 'verack' + padding
    payload_size = struct.pack('<I', 0)  # No payload, size is 0
    payload = b''  # Empty payload for 'verack'
    checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]  # Checksum of the empty payload
    verack = magic + command + payload_size + checksum # sum all data

    return verack

def decode_verack(data):
    """Decodes a verack message and verifies its structure."""
    if len(data) != 24:
        return "Error: Incomplete verack message."

    magic, command, payload_size, checksum = struct.unpack('<4s12sI4s', data[:24])
    
    # Verifying the magic bytes
    if magic != b'\xf9\xbe\xb4\xd9':
        return "Error: Incorrect magic bytes."

    # Verifying the command
    if command.strip(b'\x00') != b'verack':
        return "Error: Incorrect command."

    # Verifying the payload size
    if payload_size != 0:
        return "Error: Incorrect payload size for verack."

    # Verifying the checksum
    expected_checksum = hashlib.sha256(hashlib.sha256(b'').digest()).digest()[:4]
    if checksum != expected_checksum:
        return "Error: Incorrect checksum."

    return {
        'magic': magic.hex(),
        'command': command.strip(b'\x00').decode(),
        'payload_size': payload_size,
        'checksum': checksum.hex()
    }