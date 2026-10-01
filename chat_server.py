import socket
import threading

from rsa_core import generate_rsa_key_pair, encrypt, decrypt, string_to_key, key_to_string

HOST = "127.0.0.0"
PORT = 3334

def receive_message(client, key):
    while True:
        data = client.recv(1024)

        if not data:
            print("\n[INFO] Client disconnected.")
            break

        msg = data.decode()
        print(f"\n[Client encrypted message]: {msg}")
        print(f"\n[Client]: {decrypt(key, msg)}")

if __name__ == "__main__":
    public_key, private_key = generate_rsa_key_pair()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((HOST, PORT))
    server.listen(1)

    print(f"[INFO] Listening on port {3334}")

    client, addr = server.accept()
    print(f"[INFO] Accepted client from {addr[0]}:{addr[1]}")

    client.sendall(key_to_string(public_key).encode())
    client_pub_key = string_to_key(client.recv(1024).decode())

    print(f"Client public_key: {key_to_string(client_pub_key)}")

    bg = threading.Thread(target=receive_message, args=(client, private_key))
    bg.start()
    while True:
        msg = input("Enter a message: ")

        if msg == "quit":
            break

        client.sendall(encrypt(client_pub_key, msg).encode())

    client.close()
