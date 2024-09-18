import struct

def decode_block_header(block_data):
    block_header = block_data[:80]
    version, prev_block, merkle_root, timestamp, bits, nonce = struct.unpack('<I32s32sIII', block_header)
    
    return {
        "version": version,
        "previous_block": prev_block[::-1].hex(),
        "merkle_root": merkle_root[::-1].hex(),
        "timestamp": timestamp,
        "bits": bits,
        "nonce": nonce,
        "header_size": 80  # Tamaño fijo del encabezado del bloque
    }

def decode_compact_size(data):
    size = data[0]
    if size < 253:
        return size, 1
    elif size == 253:
        return struct.unpack('<H', data[1:3])[0], 3
    elif size == 254:
        return struct.unpack('<I', data[1:5])[0], 5
    else:
        return struct.unpack('<Q', data[1:9])[0], 9

def decode_transaction(data):
    offset = 0

    # Versión (4 bytes)
    version = struct.unpack('<I', data[offset:offset+4])[0]
    offset += 4

    # Número de inputs (Compact Size)
    input_count, input_count_size = decode_compact_size(data[offset:])
    offset += input_count_size

    inputs = []
    for _ in range(input_count):
        input_data = {}
        
        # Hash de la transacción previa (32 bytes)
        input_data['prev_tx_hash'] = data[offset:offset+32][::-1].hex()
        offset += 32

        # Índice de la salida previa (4 bytes)
        input_data['prev_tx_index'] = struct.unpack('<I', data[offset:offset+4])[0]
        offset += 4

        # Longitud del script de desbloqueo (Compact Size)
        script_length, script_length_size = decode_compact_size(data[offset:])
        offset += script_length_size

        # Script de desbloqueo
        input_data['unlocking_script'] = data[offset:offset+script_length].hex()
        offset += script_length

        # Secuencia (4 bytes)
        input_data['sequence'] = struct.unpack('<I', data[offset:offset+4])[0]
        offset += 4

        inputs.append(input_data)

    # Número de outputs (Compact Size)
    output_count, output_count_size = decode_compact_size(data[offset:])
    offset += output_count_size

    outputs = []
    for _ in range(output_count):
        output_data = {}

        # Valor (8 bytes)
        output_data['value'] = struct.unpack('<Q', data[offset:offset+8])[0]
        offset += 8

        # Longitud del script de bloqueo (Compact Size)
        script_length, script_length_size = decode_compact_size(data[offset:])
        offset += script_length_size

        # Script de bloqueo
        output_data['locking_script'] = data[offset:offset+script_length].hex()
        offset += script_length

        outputs.append(output_data)

    # Lock Time (4 bytes)
    lock_time = struct.unpack('<I', data[offset:offset+4])[0]
    offset += 4

    transaction = {
        "version": version,
        "inputs": inputs,
        "outputs": outputs,
        "lock_time": lock_time
    }

    return transaction, offset

def save_transactions_as_hex(file_path):
    with open(file_path, 'rb') as file:
        block_data = file.read()

    block_header = decode_block_header(block_data)
    header_size = block_header["header_size"]
    
    tx_count, tx_count_size = decode_compact_size(block_data[header_size:])
    print(f"Number of transactions: {tx_count}")
    
    tx_start = header_size + tx_count_size
    offset = tx_start
    
    for i in range(tx_count):
        transaction, tx_size = decode_transaction(block_data[offset:])
        
        tx_file_path = f'data/transactions/transaction_{i+1}.txt'
        with open(tx_file_path, 'w') as file:
            file.write(f"Version: {transaction['version']}\n")
            file.write(f"Inputs:\n")
            for tx_input in transaction['inputs']:
                file.write(f"  Previous Transaction Hash: {tx_input['prev_tx_hash']}\n")
                file.write(f"  Previous Transaction Index: {tx_input['prev_tx_index']}\n")
                file.write(f"  Unlocking Script: {tx_input['unlocking_script']}\n")
                file.write(f"  Sequence: {tx_input['sequence']}\n")
            file.write(f"Outputs:\n")
            for tx_output in transaction['outputs']:
                file.write(f"  Value: {tx_output['value']}\n")
                file.write(f"  Locking Script: {tx_output['locking_script']}\n")
            file.write(f"Lock Time: {transaction['lock_time']}\n")
        
        print(f"Transaction {i+1} stored in {tx_file_path}")
        offset += tx_size

def main():
    # Archivo de entrada
    input_file = 'data/block_000000000000000000026e1cfa7e5dcd97000fc579488009aebf46208e33c2f9.txt'
    
    # Guardar las transacciones en archivos independientes
    save_transactions_as_hex(input_file)

if __name__ == "__main__":
    main()
