import socket
import serial
from time import sleep

port = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=1)

UDP_IP = "127.0.0.1"
UDP_PORT = 10110

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print(data)
    port.write(data)
    sleep(0.001)
