from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import subprocess
import sys

class SecurityGatewayHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/network/inspect':
            content_length = int(self.headers['Content-Length'])
            post_data = json.loads(self.rfile.read(content_length))
            
            # Extract features safely
            p_var = post_data.get('packet_len_var', 0)
            s_count = post_data.get('sync_flag_count', 0)
            dur = post_data.get('duration_ms', 0)
            b_rate = post_data.get('byte_transfer_rate', 0)
            
            # Call our prediction model directly
            cmd = [sys.executable, 'src/predict_network.py', str(p_var), str(s_count), str(dur), str(b_rate)]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # Parse the model's stdout stream
            for line in result.stdout.split('\n'):
                if line.startswith('RESULT:'):
                    prediction, risk_score, flags = line.replace('RESULT:', '').strip().split(',')
                    
                    is_malicious = int(prediction) == 1
                    response = {
                        "status": "processed",
                        "security_alert": is_malicious,
                        "malicious_probability": float(risk_score),
                        "mitigation_action": "DROP_PACKET_AND_BAN_IP" if is_malicious else "ALLOW_ACCESS",
                        "explainable_ai_telemetry": {
                            "primary_risk_vectors": flags.split('|'),
                            "model_architecture": "Interpretable Gradient Boosting Tree Stack"
                        }
                    }
                    
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode('utf-8'))
                    return
                    
            self.send_response(500)
            self.end_headers()

if __name__ == '__main__':
    server = HTTPServer(('localhost', 4000), SecurityGatewayHandler)
    print("🛡️ Pure Python Explainable Security Engine live on port 4000...")
    server.serve_forever()