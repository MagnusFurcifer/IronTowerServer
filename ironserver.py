#!/usr/bin/env python3

import asyncio
import json
import socket
from world.game_map import GameMap, MapGenerator
import it_config
import time
import sqlite3
from sqlite3 import Error
from datetime import datetime
from datetime import timedelta
import threading
import os
import hashlib

def create_con():
    """ create a database connection to a SQLite database """
    conn = None
    try:
        print("Creating connection to DB at: " + it_config.db_path)
        conn = sqlite3.connect(it_config.db_path, check_same_thread = False)
        print(sqlite3.version)
    except Error as e:
        print(e)
    return conn

def insert_event(conn, event_text, event_date):
    print("We doin a cheeky insert: " + event_text + event_date)
    c = conn.cursor()
    c.execute("INSERT INTO events (event_text, event_date) VALUES (?, ?);", (event_text, event_date))
    print(c.lastrowid)
    conn.commit()

def insert_ghost(conn, client_id, x, y, world, level):
    c = conn.cursor()
    c.execute("DELETE FROM ghosts WHERE client_id=?;", (client_id,))
    print(c.lastrowid)
    conn.commit()
    c = conn.cursor()
    c.execute("INSERT INTO ghosts (client_id, x, y, world, level, last_update) VALUES (?, ?, ?, ?, ?, datetime('now'));", (client_id, x, y, world, level))
    print(c.lastrowid)
    conn.commit()

def create_tables(conn):
    event_table = "CREATE TABLE IF NOT EXISTS events ( " \
                    "id integer PRIMARY KEY, " \
                    "event_text text, " \
                    "event_date text " \
                    ");"
    try:
        c = conn.cursor()
        c.execute(event_table)
        conn.commit()
    except Error as e:
        print(e)
    ghost_table = "CREATE TABLE IF NOT EXISTS ghosts ( " \
                    "id integer PRIMARY KEY, " \
                    "client_id text, " \
                    "x int, " \
                    "y int, " \
                    "world text, " \
                    "level int, " \
                    "last_update text" \
                    ");"
    try:
        c = conn.cursor()
        c.execute(ghost_table)
        conn.commit()
    except Error as e:
        print(e)

def get_events(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM events")
    rows = c.fetchall()
    return rows

def get_ghosts(conn, world, level):
    c = conn.cursor()
    c.execute("SELECT * FROM ghosts WHERE world=? AND level=? LIMIT 10", (world, level))
    rows = c.fetchall()
    return rows

def parse_ghosts(client_id, rows):
    resp = {
        "TYPE"      :       "GHOSTS"
    }
    ghost_list = []
    for row in rows:
        if row[1] != client_id:
            tmp_ghost = {
                "x"     :       row[2],
                "y"     :       row[3]
            }
            ghost_list.append(tmp_ghost)
    resp["GHOST_LIST"] = ghost_list
    return resp

def delete_old_ghosts(conn):
    print("DELETING OLD GHOSTS")
    c = conn.cursor()
    c.execute("DELETE FROM ghosts WHERE (last_update <= datetime('now', '-1 minutes'))")
    conn.commit()

def worker_proc():
    con = create_con()
    rows = get_events(con)
    path = it_config.ironweb_path + "index.html"
    results = []
    for row in rows:
        results.append(row[1] + " " + row[2])
    page = "<html>"
    page = page + "<br>".join(results)
    page = page + "</html>"
    with open(path, "w") as f:
        f.write(page)
    #Clean up old GHOSTS
    con = create_con()
    delete_old_ghosts(con)

def start_worker():
    while True:
        worker_proc()
        time.sleep(60)

#Game Server
async def echo_server(reader, writer):
    data = await reader.read(1000)  # Max number of bytes to read
    message = data.decode()
    try:
        command = json.loads(message)
    except json.JSONDecodeError:
        command = "Invalid Command"
    addr = writer.get_extra_info('peername')
    print("Connection from: " + str(addr) + " - Command: " + str(command))
    event = None
    if command.get("COMMAND") == "MAPGEN":
        MapGen = MapGenerator(command.get("TYPE"), command.get("LEVEL"))
        gendmap = MapGen.generate_map()
        writer.write(json.dumps(gendmap).encode())
        await writer.drain()  # Flow control, see later
    elif command.get("COMMAND") == "EVENT":
        if command.get("TYPE") == "ASCEND":
            event =  str(command.get("ASC_PNAME")) + " has ascneded to level " + str(command.get("ASC_LEVEL")) + " of the " + str(command.get("ASC_TYPE"))
    elif command.get("COMMAND") == "TICK":
        id_string = str(addr[0]) + command.get("NAME")
        client_id = hashlib.sha1(id_string.encode()).hexdigest()
        con = create_con()
        insert_ghost(con, client_id, command.get("x"), command.get("y"), command.get("WORLD"), command.get("LEVEL"))
        g = get_ghosts(con, command.get("WORLD"), command.get("LEVEL"))
        print(g)
        pg = parse_ghosts(client_id, g)
        print(pg)

        writer.write(json.dumps(pg).encode())
        await writer.drain()
    writer.close()
    if event is not None:
        print("Inserting event: " + event)
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        con = create_con()
        insert_event(con, str(event), date_time)

async def main(host, port):
    server = await asyncio.start_server(echo_server, host, port)
    async with server:
        await server.serve_forever()

#DB init
con = create_con()
create_tables(con)
#Thread that updates the website dir
daemon = threading.Thread(name='IronTower Worker',target=start_worker)
daemon.setDaemon(True)
daemon.start()
#Start Game Server
asyncio.run(main(it_config.ironserver_host, it_config.ironserver_port))
