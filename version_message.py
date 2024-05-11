# version-message.py 
# is a code of presentation between nodes
'''
Payload (version message):
┌───────────────────────┬─────────────────────┬────────────────────────────┬─────────┬─────────────────────────────────────────────────┐
│ Name                  │ Example Data        │ Format                     │    Size │ Example Bytes                                   │
├───────────────────────┼─────────────────────┼────────────────────────────┼─────────┼─────────────────────────────────────────────────┤
│ Protocol Version      │ 70014               │ little-endian              │       4 │ 7E 11 01 00                                     │
│ Services              │ 0                   │ bit field, little-endian   │       8 │ 00 00 00 00 00 00 00 00                         │
│ Time                  │ 1640961477          │ little-endian              │       8 │ C5 15 CF 61 00 00 00 00                         │
│ Remote Services       │ 0                   │ bit field, little-endian   │       8 │ 00 00 00 00 00 00 00 00                         │
│ Remote IP             │ 64.176.221.94       │ ipv6, big-endian           │      16 │ 00 00 00 00 00 00 00 00 00 00 FF FF 2E 13 89 4A │
│ Remote Port           │ 8333                │ big-endian                 │       2 │ 20 8D                                           │
│ Local Services        │ 0                   │ bit field, little-endian   │       8 │ 00 00 00 00 00 00 00 00                         │
│ local IP              │ 127.0.0.1           │ ipv6, big-endian           │      16 │ 00 00 00 00 00 00 00 00 00 00 FF FF 7F 00 00 01 │
│ Local Port            │ 8333                │ big-endian                 │       2 │ 20 8D                                           │
│ Nonce                 │ 0                   │ little-endian              │       8 │ 00 00 00 00 00 00 00 00                         │
│ User Agent            │ ""                  │ compact size, ascii        │ compact │ 00                                              │
│ Last Block            │ 0                   │ little-endian              │       4 │ 00 00 00 00                                     │
└───────────────────────┴─────────────────────┴────────────────────────────┴─────────┴─────────────────────────────────────────────────┘
'''
import socket
import struct
import time
import hashlib

def create_version_message():
    # Define the values for each field
    protocol_version = 70015
    services = 0
    timestamp = int(time.time())
    remote_services = 0
    remote_ip = '64.176.221.94'  
    remote_port = 8333
    local_services = 0
    local_ip = '127.0.0.1'
    local_port = 8333
    nonce = 0
    user_agent = b""
    last_block = 0

    # Pack the data into binary format
    version_payload = struct.pack('<I', protocol_version)
    version_payload += struct.pack('<Q', services)
    version_payload += struct.pack('<Q', timestamp)
    version_payload += struct.pack('<Q', remote_services)
    version_payload += struct.pack('>16s', socket.inet_pton(socket.AF_INET6, '::ffff:' + remote_ip))
    version_payload += struct.pack('>H', remote_port)
    version_payload += struct.pack('<Q', local_services)
    version_payload += struct.pack('>16s', socket.inet_pton(socket.AF_INET6, '::ffff:' + local_ip))
    version_payload += struct.pack('>H', local_port)
    version_payload += struct.pack('<Q', nonce)
    version_payload += struct.pack('B', len(user_agent)) + user_agent
    version_payload += struct.pack('<I', last_block)

    # Build the complete message with header
    command = b'version' + b'\x00' * (12 - len(b'version'))  # Command is 'version', padded to 12 bytes
    length = struct.pack('I', len(version_payload))
    checksum = hashlib.sha256(hashlib.sha256(version_payload).digest()).digest()[:4]
    message = b'\xf9\xbe\xb4\xd9' + command + length + checksum + version_payload  # the first character correspont to the famous magic number or magic bytes

    return message
