import http.server
import socketserver
import json
import os
import requests
from urllib.parse import urlparse

PORT = 3000
DIRECTORY = "/Users/kmtwarrior/clawd/lead_system/landing_pages/micro-niche-finder"

def load_env():
    env = {}
    env_path = os.path.join(DIRECTORY, '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    env[key] = value
    return env

config = load_env()
BREVO_API_KEY = config.get("BREVO_API_KEY")
BREVO_LIST_ID = 59 # Niche finder list

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_POST(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/api/subscribe':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                email = data.get('email')
                keyword = data.get('keyword')
                
                print(f"Received subscription request for: {email}, keyword: {keyword}")
                
                # Call Brevo API
                brevo_url = "https://api.brevo.com/v3/contacts"
                headers = {
                    "accept": "application/json",
                    "api-key": BREVO_API_KEY,
                    "content-type": "application/json"
                }
                payload = {
                    "email": email,
                    "listIds": [BREVO_LIST_ID],
                    "updateEnabled": True,
                    "attributes": {
                        "SOURCE": "SignalEngines_LP",
                        "INTEREST": keyword or "General"
                    }
                }
                
                response = requests.post(brevo_url, headers=headers, json=payload)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                
                if response.status_code in [200, 201, 204]:
                     self.wfile.write(json.dumps({"success": True, "message": "Contact added"}).encode('utf-8'))
                else:
                    # Check for duplicate
                    try:
                        err_json = response.json()
                        if err_json.get('code') == 'duplicate_parameter':
                             self.wfile.write(json.dumps({"success": True, "message": "Contact updated"}).encode('utf-8'))
                        else:
                             print(f"Brevo Error: {response.text}")
                             self.wfile.write(json.dumps({"success": False, "error": response.text}).encode('utf-8'))
                    except:
                        self.wfile.write(json.dumps({"success": False, "error": response.text}).encode('utf-8'))

            except Exception as e:
                print(f"Error processing request: {e}")
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
                
        else:
            self.send_error(404, "API endpoint not found")

print(f"Starting server at http://localhost:{PORT}")
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()
