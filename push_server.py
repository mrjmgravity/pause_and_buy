from flask import Flask, request, jsonify, send_from_directory
from pywebpush import webpush, WebPushException
import json
import os

# Set these environment variables or edit directly (not recommended for production)
VAPID_PRIVATE_KEY = os.environ.get('VAPID_PRIVATE_KEY')
VAPID_PUBLIC_KEY = os.environ.get('VAPID_PUBLIC_KEY')
VAPID_CLAIMS = {"sub": "mailto:you@example.com"}

app = Flask(__name__, static_folder='web', static_url_path='')

# Simple in-memory store for subscriptions (replace with DB in production)
subscriptions = []

@app.route('/')
def index():
    return send_from_directory('web', 'index.html')

@app.route('/manifest.json')
def manifest():
    return send_from_directory('web', 'manifest.json')

@app.route('/sw.js')
def sw():
    return send_from_directory('web', 'sw.js')

@app.route('/vapid_public')
def vapid_public():
    return jsonify({'publicKey': VAPID_PUBLIC_KEY})

@app.route('/save-subscription', methods=['POST'])
def save_subscription():
    sub = request.get_json()
    if sub not in subscriptions:
        subscriptions.append(sub)
    return ('', 204)

@app.route('/send-notification', methods=['POST'])
def send_notification():
    data = request.get_json()
    payload = json.dumps({'title': data.get('title','Pause & Buy'), 'body': data.get('body','Máte notifikáciu')})
    failed = []
    for sub in subscriptions:
        try:
            webpush(sub, payload, vapid_private_key=VAPID_PRIVATE_KEY, vapid_claims=VAPID_CLAIMS)
        except WebPushException as ex:
            failed.append(str(ex))
    return jsonify({'sent': len(subscriptions)-len(failed), 'failed': failed})

if __name__ == '__main__':
    if not VAPID_PUBLIC_KEY or not VAPID_PRIVATE_KEY:
        print('VAPID keys not set. Generate them before running (see README).')
    app.run(host='0.0.0.0', port=5000, debug=True)
