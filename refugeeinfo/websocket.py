from __future__ import absolute_import, unicode_literals, division, print_function

__author__ = 'reyrodrigues'

from tornado import websocket

clients = []


class WSHandler(websocket.WebSocketHandler):

    def open(self):
        clients.append(self)
        print('connection opened...')

    def on_message(self, message):
        # application logic
        print('received:', message)
        self.write_message("Roger that")

    def on_close(self):
        clients.remove(self)
        print('connection closed...')