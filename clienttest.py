#!/usr/bin/env python3
import sys
import json
import socket
import it_config

cmd = {
    "COMMAND"   :   "MAPGEN",
    "TYPE"      :   "DUNGEON",
    "LEVEL"     :   "1"
}

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((it_config.ironserver_host, it_config.ironserver_port))
    s.sendall(json.dumps(cmd).encode())
    print("Command Sent")
    data = []
    while True:
        packet = s.recv(4096)
        print(packet)
        if not packet: break
        data.append(packet)
    s.close()
    data_join = b"".join(data)
    rec_map = json.loads(data_join)
    print(rec_map)
