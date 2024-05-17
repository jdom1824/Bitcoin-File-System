import struct

def decode_verack(data):
    header_format = '<4s12sI4s'  # Magic, Command, Size, Checksum
    header_size = struct.calcsize(header_format)
    
    if len(data) < header_size:
        return "Error: Data too short for a message header."
    
    magic, command, size, checksum = struct.unpack(header_format, data[:header_size])
    
    if command.strip(b'\x00').decode() != 'verack':
        return "Error: Incorrect command for verack message."
    
    if size != 0:
        return "Error: verack message should have no payload."
    
    return {
        "magic": magic.hex(),
        "command": command.decode('ascii').rstrip('\x00'),
        "size": size,
        "checksum": checksum.hex()
    }
