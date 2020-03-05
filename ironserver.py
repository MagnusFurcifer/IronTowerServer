#!/usr/bin/env python3

import asyncio
import json
import socket
from world.game_map import GameMap, MapGenerator
import it_config
import SimpleHTTPServer
import SocketServer
import sqlite3
from sqlite3 import Error
from datetime import datetime


def create_con():
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(it_config.db_path, check_same_thread = False)
        print(sqlite3.version)
    except Error as e:
        print(e)
    return conn

def insert_event(conn, event_text, event_date):
    sql = "INSERT INTO events (event_text, event_date) VALUES (" + \
            event_text + "," + \
            event_date + \
            ")"
    c = conn.cursor()
    c.execute(sql)

def create_tables(conn):
    event_table = "CREATE TABLE IF NOT EXISTS events ( " \
                    "id integer PRIMARY KEY, " \
                    "event_text text, " \
                    "event_date text " \
                    ");"
    try:
        c = conn.cursor()
        c.execute(event_table)
    except Error as e:
        print(e)

def get_events(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM events")
    rows = c.fetchall()
    return rows

#Web server
def start_web_server():
    os.chdir(it_config.ironweb_path)
    httpd = HTTPServer(('', it_config.ironweb_port), CGIHTTPRequestHandler)
    httpd.serve_forever()

def worker_proc():
    con = create_con()
    rows = get_events(con)
    path = it_config.ironweb_path + "index.html"
    with open(path, "w") as f:
        f.write("\n".join(rows))

def start_worker():
    while True:
        worker_proc()
        time.sleep(60)

#Game Server
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
        MapGen = MapGenerator(it_config.map_width, it_config.map_height, command.get("TYPE"), command.get("LEVEL"))
        gendmap = MapGen.generate_map(it_config.max_rooms, it_config.room_min_size, it_config.room_max_size)
    writer.write(json.dumps(gendmap).encode())
    await writer.drain()  # Flow control, see later
    writer.close()
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    con = create_con()
    insert_event(con, str(command), date_time)

async def main(host, port):
    server = await asyncio.start_server(echo_server, host, port)
    async with server:
        await server.serve_forever()

#DB
con = create_con()
create_tables(con)
#Start Web server
daemon = threading.Thread(name='IronTower Web Server',target=start_web_server)
daemon.setDaemon(True)
daemon.start()
#Thread that updates the website
daemon = threading.Thread(name='IronTower Worker',target=start_worker)
daemon.setDaemon(True)
daemon.start()
#Start Game Server
asyncio.run(main(it_config.ironserver_host, it_config.ironserver_port))
