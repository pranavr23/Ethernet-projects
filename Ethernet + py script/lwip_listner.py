import socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to the server; enter your server's IP and port here, as
#  printed by the board's serial interface
client.connect(("192.168.1.10", 7))
# specify the number of bytes we're requesting from the server
# change this as desired, several values up to 50k have been tested
# for much more, more than two bytes would need to be used to
#  specify length
num_bytes = 500

# arbitrary packet size, max number of bytes we'll receive at once
packet_size = 256

# send two bytes representing num_bytes to request that many bytes
#  in response
# note: little endian is important, requirement for Zynq-7000 to
#       easily translate the sent number to an int without reordering
print(f"requesting {num_bytes.to_bytes(2, 'little')} bytes")
client.send(num_bytes.to_bytes(2, 'little'))

# loop while calling recv to receive data from the client until the
# expected number of bytes has been successfully transferred
received = 0
errors = 0
while received < num_bytes:
    data = client.recv(packet_size)
    for d in range(len(data)):
        expected_value = (received + d) & 0xff
        if data[d]!= expected_value: # validate data
            print(f"Error, data[{d}] ({data[d]}) != {expected_value}")
            errors += 1
    received += len(data)
    print(f"Received {received} bytes total, {len(data)} in this recv")
if errors == 0:
    print("All data received matched the expected values!")
else:
    print(f"{errors} errors")