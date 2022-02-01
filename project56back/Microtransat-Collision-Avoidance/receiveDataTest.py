import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 10110

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    # print("received message: %s" % data)
    # data = data[2:]
    data = data.strip(b'\n')
    # data = data.strip(b'\r')
    # data = data[:1]
    # print(data)
    print(data.decode(encoding="ascii"))
