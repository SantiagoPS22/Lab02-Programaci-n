import requests
from http.server import BaseHTTPRequestHandler, HTTPServer

BACKEND = "http://127.0.0.1:80"
GET_ROUTES = {"list_student_labs", "list_professors_labs", "list_students", "download_lab"}

class Puente(BaseHTTPRequestHandler):
    def do_GET(self):
        # Entrega la página HTML
        with open("client/index.html", "rb") as f:
            html = f.read()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(html)))
        self.end_headers()
        self.wfile.write(html)

    def do_POST(self):
        # Recibe lo que manda el JavaScript y lo reenvía al servidor real
        route = self.path.replace("/api/", "")
        body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        headers = {h: self.headers[h] for h in ("X-File-Name", "X-Client-ID") if self.headers.get(h)}
        if route in GET_ROUTES:
            r = requests.get(BACKEND + "/" + route, data=body, headers=headers)
        else:
            r = requests.post(BACKEND + "/" + route, data=body, headers=headers)
        self.send_response(r.status_code)
        self.send_header("Content-Length", str(len(r.content)))
        self.end_headers()
        self.wfile.write(r.content)

HTTPServer(("127.0.0.1", 8000), Puente).serve_forever()