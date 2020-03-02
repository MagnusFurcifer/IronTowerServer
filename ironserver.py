#!/usr/bin/env python3

import asyncio
import json
import socket
from world.game_map import GameMap, MapGenerator
import it_config


async def echo_server(reader, writer):
    data = await reader.read(100)  # Max number of bytes to read
    message = data.decode()
    try:
        command = json.loads(message)
    except json.JSONDecodeError:
        command = "Invalid Command"
    addr = writer.get_extra_info('peername')
    print("Connection from: " + str(addr) + " - Command: " + str(command))
    if command.get("COMMAND") == "MAPGEN":
        MapGen = MapGenerator(it_config.map_width, it_config.map_height)
        gendmap = MapGen.generate_map(command.get("TYPE"), command.get("LEVEL"), it_config.max_rooms, it_config.room_min_size, it_config.room_max_size)
    writer.write(json.dumps(gendmap).encode())
    await writer.drain()  # Flow control, see later
    writer.close()

async def main(host, port):
    server = await asyncio.start_server(echo_server, host, port)
    async with server:
        await server.serve_forever()
asyncio.run(main(it_config.ironserver_host, it_config.ironserver_port))
