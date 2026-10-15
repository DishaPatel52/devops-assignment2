from flask import Flask, jsonify, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import time

app = Flask(__name__)
START_TIME = time.time()

# Prometheus Metric
REQUEST_COUNT = Counter('app_http_requests_total', 'Total HTTP Requests', ['method', 'endpoint', 'status'])

@app.route('/')
def home():
    REQUEST_COUNT.labels(method='GET', endpoint='/', status='200').inc()
    return jsonify({
        "status": "online",
        "service": "Attendance Analytics & DevOps Portal",
        "version": "2.0.0"
    })

@app.route('/health')
def health():
    REQUEST_COUNT.labels(method='GET', endpoint='/health', status='200').inc()
    return jsonify({
        "status": "healthy",
        "uptime": round(time.time() - START_TIME, 2)
    }), 200

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)