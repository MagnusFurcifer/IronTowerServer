#!/usr/bin/env python3

import socket
import pickle

#Setup world and entities
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 8080        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    cmd = {
    "COMMAND"   :   "GEN_DUNGEON",
    "LEVEL"     :   "1"
    }

    s.sendall(pickle.dumps(cmd) + "\0")
    print("Command Sent")

    data = []
    while True:
        packet = s.recv(4096)
        print(packet)
        if not packet: break
        data.append(packet)
    s.close()
    data_join = b"".join(data)
    rec_map = pickle.loads(data_join)
    print(rec_map)
