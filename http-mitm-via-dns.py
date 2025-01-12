import argparse
import ssl
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
class ProxyHandler(BaseHTTPRequestHandler):
    def do_request(self, method):
        global hedef_url
        protokol = "https" if self.server.secure else "http"
        host = self.headers['Host']
        if re.search(r":\d+$", host):
            hedef_url = f"{protokol}://{host}{self.path}"
        else:
            hedef_url = f"{protokol}://{host}:{self.server.target_port}{self.path}"
        headers = dict(self.headers)
        data = None
        if "Content-Length" in headers:
            content_length = int(headers["Content-Length"])
            data = self.rfile.read(content_length)
        response = requests.request(
            method,
            hedef_url,
            headers=headers,
            data=data,
            verify=False,
            proxies=self.server.proxies
        )
        self.send_response(response.status_code)
        for key, value in response.headers.items():
            if key.lower() != 'transfer-encoding':
                self.send_header(key, value)
        self.end_headers()
        self.wfile.write(response.content)
    def do_GET(self):
        self.do_request("GET")
    def do_POST(self):
        self.do_request("POST")
    def do_PUT(self):
        self.do_request("PUT")
    def do_DELETE(self):
        self.do_request("DELETE")
    def do_OPTIONS(self):
        self.do_request("OPTIONS")
    def do_TRACE(self):
        self.do_request("TRACE")
    def do_TRACK(self):
        self.do_request("TRACK")
def run(server_class=HTTPServer, handler_class=ProxyHandler, port=8080, target_port=80, proxy_host=None, proxy_port=None, certfile=None, keyfile=None):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.target_port = target_port
    httpd.certfile = certfile
    httpd.keyfile = keyfile
    httpd.proxies = {
        "http": f"http://{proxy_host}:{proxy_port}" if proxy_host and proxy_port else None,
        "https": f"http://{proxy_host}:{proxy_port}" if proxy_host and proxy_port else None
    }
    if certfile and keyfile:
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain(certfile=certfile, keyfile=keyfile)
        httpd.socket = ssl_context.wrap_socket(httpd.socket, server_side=True)
        httpd.secure = True
    else:
        httpd.secure = False
    httpd.serve_forever()
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DNS tabanlı HTTP/HTTPS MITM Aracı")
    parser.add_argument("--port", type=int, required=True, help="Dinlenecek port numarası ")
    parser.add_argument("--proxy-host", type=str, help="Proxy sunucu IP adresi ")
    parser.add_argument("--proxy-port", type=int, help="Proxy sunucu port numarası ")
    parser.add_argument("--certfile", type=str, help="SSL sertifika dosyası (.pem türünde)")
    parser.add_argument("--keyfile", type=str, help="SSL anahtar dosyası (.pem türünde)")
    args = parser.parse_args()
    run(
        port=args.port,
        target_port=args.port,
        proxy_host=args.proxy_host,
        proxy_port=args.proxy_port,
        certfile=args.certfile,
        keyfile=args.keyfile
    )
