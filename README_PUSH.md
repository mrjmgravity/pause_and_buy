Pause & Buy — PWA + Web Push (for Android / TWA)

Overview
- This folder provides a simple Progressive Web App (PWA) front-end and a Flask-based push server using Web Push (VAPID).
- You can host the `web/` folder on HTTPS and wrap the site as an Android Trusted Web Activity (TWA) to publish on Google Play.

Quick start (development)
1. Create VAPID keys (one-time):
   ```bash
   pip install pywebpush
   python - <<PY
   from pywebpush import generate_vapid_key
   print(generate_vapid_key())
   PY
   ```
   Save the keys and set env vars:
   ```powershell
   $env:VAPID_PRIVATE_KEY='...'
   $env:VAPID_PUBLIC_KEY='...'
   ```

2. Install server dependencies:
```powershell
python -m pip install -r requirements-push.txt
```

3. Run server (HTTPS required for real push; for local testing use ngrok):
```powershell
python push_server.py
```

4. Open your site (http://localhost:5000) in Chrome on Android (or expose via ngrok and open HTTPS URL). Click "Povoliť notifikácie" to subscribe.

Sending test notification
POST JSON to `/send-notification`:
```bash
curl -X POST http://localhost:5000/send-notification -H "Content-Type: application/json" -d '{"title":"Test","body":"Hello from server"}'
```

Wrap as Android TWA (for Play Store)
- Use Bubblewrap (recommended) to create an Android project that launches your hosted PWA as a Trusted Web Activity.
- Follow Bubblewrap docs: https://github.com/GoogleChromeLabs/bubblewrap
- You will need to set up Digital Asset Links on your hosting domain and configure the app signing.

Firebase (optional)
- If you want native push (FCM) with more reliability/background delivery, integrate Firebase Cloud Messaging into an Android app and forward web events or tokens to your server.

Security & production
- Use a real database for subscriptions.
- Protect endpoints and rotate VAPID keys as needed.
- Serve over HTTPS.

If you want, I can:
- Add icons to `web/icons/` and build more complete manifest.
- Create a Bubblewrap configuration and example commands to generate the Android project for your domain.
