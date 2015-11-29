from __future__ import absolute_import, unicode_literals, division, print_function

__author__ = 'reyrodrigues'

from tornado.options import options, define, parse_command_line
import logging
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi
import os
import refugeeinfo.wsgi
from refugeeinfo.websocket import WSHandler, clients

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

define('port', type=int, default=8080)
tornado.options.parse_command_line()


class HelloHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello from tornado')
        for c in clients:
            c.write_message('Hello from tornado')


def main():
    logger = logging.getLogger(__name__)
    wsgi_app = tornado.wsgi.WSGIContainer(
        refugeeinfo.wsgi.application)
    tornado_app = tornado.web.Application(
        [
            ('/ws', WSHandler),
            ('.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app)),
        ], debug=True)
    logger.info("Tornado server starting...")
    server = tornado.httpserver.HTTPServer(tornado_app)
    server.listen(options.port)
    # start_cleaning()
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()