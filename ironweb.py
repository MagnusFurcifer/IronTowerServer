#!/usr/bin/env python3
import http.server
import socketserver
import it_config

os.chdir(it_config.ironweb_path)
with socketserver.TCPServer(('', it_config.ironweb_port), http.server.SimpleHTTPRequestHandler) as httpd:
	httpd.serve_forever()
