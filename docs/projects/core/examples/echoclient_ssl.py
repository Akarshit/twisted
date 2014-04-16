#!/usr/bin/env python
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

if __name__ == '__main__':
    import echoclient_ssl
    raise SystemExit(echoclient_ssl.main())

from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet import ssl, reactor


class EchoClient(LineReceiver):
    end="Bye-bye!"
    def connectionMade(self):
        self.sendLine("Hello, world!")
        self.sendLine("What a fine day it is.")
        self.sendLine(self.end)

    def connectionLost(self, reason):
        print 'connection lost (protocol)'

    def lineReceived(self, line):
        print "receive:", line
        if line==self.end:
            self.transport.loseConnection()

class EchoClientFactory(ClientFactory):
    protocol = EchoClient

    def clientConnectionFailed(self, connector, reason):
        print 'connection failed:', reason.getErrorMessage()
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print 'connection lost:', reason.getErrorMessage()
        reactor.stop()

def main():
    factory = EchoClientFactory()
    with open('public.pem') as certFile:
        authority = ssl.Certificate.loadPEM(certFile.read())
    reactor.connectSSL('localhost', 8000, factory,
                       ssl.settingsForClientTLS(u'example.com',
                                                authority))
    reactor.run()
