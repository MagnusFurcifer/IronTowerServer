#!/usr/bin/env python3
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
import sys
import json

#Setup world and entities
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 8080        # The port used by the server
cmd = {
    "COMMAND"   :   "MAPGEN",
    "TYPE"      :   "DUNGEON",
    "LEVEL"     :   "1"
}



class EchoClient(LineReceiver):
    def connectionMade(self):
        self.sendLine(json.dumps(cmd).encode())

    def lineReceived(self, line):
        print("Received")
        print(json.loads(line))
        self.transport.loseConnection()

class EchoClientFactory(ClientFactory):
    protocol = EchoClient

    def clientConnectionFailed(self, connector, reason):
        print('connection failed:' + reason.getErrorMessage())
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print('connection lost:' + reason.getErrorMessage())
        reactor.stop()

def main():
    factory = EchoClientFactory()
    reactor.connectTCP(HOST, PORT, factory)
    reactor.run()

if __name__ == '__main__':
    main()
