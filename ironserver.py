#!/usr/bin/env python3
import socket
import json
import asyncio

from world.game_map import GameMap, MapGenerator
import it_config

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 8080        # Port to listen on (non-privileged ports are > 1023)

MapGen = MapGenerator(it_config.map_width, it_config.map_height)
gendmap = MapGen.generate_map(it_config.max_rooms, it_config.room_min_size, it_config.room_max_size, it_config.map_width, it_config.map_height)
map = {
    "COMMAND"   :   "MAPDATA",
    "WIDTH"     :   gendmap.width,
    "HEIGHT"    :   gendmap.height,
    "TILES"     :   gendmap.tiles.__dict__,
    "PLAYERX"   :   gendmap.playerX,
    "PLAYERY"   :   gendmap.playerY
    }

async def echo_server(reader, writer):
    while True:
        data = await reader.read(100)  # Max number of bytes to read
        if not data:
            break
    writer.write(json.dumps(map).encode())
    await writer.drain()  # Flow control, see later
    writer.close()

async def main(host, port):
    server = await asyncio.start_server(echo_server, host, port)
    await server.serve_forever()

asyncio.run(main(HOST, PORT))
