import socket
import threading

from rsa_core import generate_rsa_key_pair, encrypt, decrypt, string_to_key, key_to_string


HOST = "127.0.0.0"
PORT = 3334

def receive_message(client, key):
    while True:
        data = client.recv(1024)

        if not data:
            print("\n[INFO] disconnected.")
            break

        msg = data.decode()

        print(f"\n[Server encrypted message]: {msg}")
        print(f"\n[Server]: {decrypt(key, msg)}")


if __name__ == "__main__":
    public_key, private_key = generate_rsa_key_pair()

    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((HOST, PORT))

    conn.sendall(key_to_string(public_key).encode())
    server_pub_key = string_to_key(conn.recv(1024).decode())

    print(f"Server public_key: {key_to_string(server_pub_key)}")

    bg = threading.Thread(target=receive_message, args=(conn, private_key))
    bg.start()

    while True:
        msg = input("Enter a message: ")

        if msg == "quit":
            break

        conn.sendall(encrypt(server_pub_key, msg).encode())

    conn.close()
