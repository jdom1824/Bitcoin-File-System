import struct
import socket

def decode_version_message(data):
    header_format = '<4s12sI4s'  # Magic, Command, Size, Checksum
    header_size = struct.calcsize(header_format)
    version_details_format = '<IQQQ16sHQ16sHQ'  # Hasta Nonce incluido
    version_details_size = struct.calcsize(version_details_format)

    if len(data) < header_size:
        return "Error: Data too short for a message header."
    
    magic, command, size, checksum = struct.unpack(header_format, data[:header_size])
    if len(data) < header_size + size:
        return "Error: Data too short for the announced payload size."
    
    payload = data[header_size:header_size + size]
    if len(payload) < version_details_size:
        return "Error: Payload too short to include all fixed-size fields."

    unpacked_data = struct.unpack(version_details_format, payload[:version_details_size])

    user_agent_length = struct.unpack_from('B', payload, version_details_size)[0]
    user_agent_start = version_details_size + 1

    if len(payload) < user_agent_start + user_agent_length:
        return "Error: Payload too short for the declared user agent length."

    user_agent = struct.unpack_from(f'{user_agent_length}s', payload, user_agent_start)[0].decode()

    last_block_start = user_agent_start + user_agent_length
    if len(payload) < last_block_start + 4:
        return "Error: Payload too short to include last block."

    last_block = struct.unpack_from('<I', payload, last_block_start)[0]

    return {
        "magic": magic.hex(),
        "command": command.decode('ascii').rstrip('\x00'),
        "protocol_version": unpacked_data[0],
        "services": unpacked_data[1],
        "timestamp": unpacked_data[2],
        "remote_services": unpacked_data[3],
        "remote_ip": socket.inet_ntop(socket.AF_INET6, unpacked_data[4]),
        "remote_port": unpacked_data[5],
        "local_services": unpacked_data[6],
        "local_ip": socket.inet_ntop(socket.AF_INET6, unpacked_data[7]),
        "local_port": unpacked_data[8],
        "nonce": unpacked_data[9],
        "user_agent": user_agent,
        "last_block": last_block
    }
