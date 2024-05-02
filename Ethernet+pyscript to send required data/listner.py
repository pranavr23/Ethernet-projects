import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to the server; enter your server's IP and port here
client.connect(("192.168.1.10", 7))

# specify the number of bytes we're requesting from the server
num_bytes = 5  # 80085 has 5 bytes

# send two bytes representing num_bytes to request that many bytes in response
print(f"Requesting {num_bytes} bytes")
client.send(num_bytes.to_bytes(2, 'little'))

# receive and validate the data
received_data = b""
expected_data = b"80085"
while len(received_data) < num_bytes:
    data = client.recv(num_bytes - len(received_data))
    if not data:
        break
    received_data += data

# validate received data
if received_data == expected_data:
    print("Received data matches the expected value: '80085'!")
else:
    print("Error: Received data does not match the expected value.")

client.close()
