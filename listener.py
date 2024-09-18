#listener.py
from utils import receive_message, close_socket
from split_message import process_message
from handle_pong import send_pong
from ping import decode_ping
from decode_inv_data import decode_inv
from get_block_hash import request_block_data, save_block_to_file

def listen_for_messages(sock, ip):
    block_hash = '000000000000000000026e1cfa7e5dcd97000fc579488009aebf46208e33c2f9'
    file_path = f'data/block_{block_hash}.txt'
    try:
        print(f"Listening for messages from {ip}...")
        while True:
            response = receive_message(sock)
            if response:
                messages = process_message(response)
                for message in messages:
                    print(f"Received message type: {message['type']}")
                    if message['type'] == 'ping':
                        # Obtener el nonce directamente del mensaje sin decodificar
                        nonce_bytes, error = decode_ping(message)
                        if error:
                            print(error)
                        else:
                            print(f"Sending pong with nonce: {nonce_bytes.hex()}")
                            send_pong(sock, nonce_bytes)
                            request_block_data(sock, block_hash)
                    elif message['type'] == 'inv':
                        inv_message, error = decode_inv(message['message'])
                        if error:
                            print(error)
                        else:
                            print(f"Received inv message: {inv_message}")
                    elif message['type'] == 'block':
                        save_block_to_file(message['message'][24:], file_path)
            else:
                print("No more data received. Connection may be closed.")
                break
    except Exception as e:
        print(f"An error occurred while listening for messages from {ip}: {e}")
    finally:
        close_socket(sock)
        print(f"Listening socket to {ip} closed.")
