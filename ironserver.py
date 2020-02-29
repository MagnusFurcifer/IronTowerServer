#!/usr/bin/env python3
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
from twisted.protocols.basic import LineReceiver
import json
from world.game_map import GameMap, MapGenerator
import it_config

# This is just about the simplest possible protocol
class Echo(LineReceiver):
    def connectionMade(self):
        self.factory.clients.append(self)

    def connectionLost(self, reason):
        self.factory.clients.remove(self)

    def lineReceived(self, data):
        command = json.loads(data)
        print("Received command: " + str(command))
        if command.get("COMMAND") == "MAPGEN":
            MapGen = MapGenerator(it_config.map_width, it_config.map_height)
            map = MapGen.generate_map(it_config.max_rooms, it_config.room_min_size, it_config.room_max_size, it_config.map_width, it_config.map_height)
            print(map)
            self.sendLine(json.dumps(map).encode())

PORT = 8080
f = Factory()
f.protocol = Echo
f.clients = []
reactor.listenTCP(PORT, f)
reactor.run()
