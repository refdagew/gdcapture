# GDCapture

A Geometry Dash capture and streaming project.

## Current target

- Geometry Dash: Windows 2.2081
- Geode SDK: 5.11.2
- Build target: Windows x64 (Win64)

## Build

GitHub Actions builds the Windows Geode package on pushes to `main`, pull requests, and manual workflow dispatches.

Download the `GDCapture-Win64` artifact from the workflow run.

## Firebase web app

The initial web UI lives in `web/index.html`. Firebase configuration is initialized in that file using the project config supplied for GDCapture.

Before using the page:

1. In Firebase Console, enable **Authentication → Sign-in method → Anonymous**.
2. Create the Cloud Firestore database.
3. Deploy the rules in `firestore.rules`.
4. Deploy Hosting from the repository root with the Firebase CLI: `firebase deploy --only firestore:rules,hosting`.

The root `firebase.json` configures Hosting to serve the `web/` directory and points Firestore at `firestore.rules`. `firebase-rules.json` is a copy of that JSON configuration for reference; Firestore security rules themselves are the plain-text `firestore.rules` file.

## Local WebSocket server (macOS)

From the repository root, run:

```bash
python3 -m pip install -r server/requirements.txt
python3 server/server.py
```

The server listens only on `127.0.0.1`: browser WebSocket on port `8765`, and a local HTTP handshake endpoint for the Geode mod on port `8766`. Open the hosted GDCapture page on the same Mac, click **Connect local server**, and look for **WebSocket round-trip successful**. Start Geometry Dash with the updated Geode mod installed; the server terminal should print `GEODE MOD CONNECTED`. Stop the server with Ctrl+C.

This is a connectivity test only. It does not capture Geometry Dash frames or stream video yet.

## Current development status

The first mod milestone is a loadable Geode skeleton. The web page currently supports anonymous Firebase sign-in, creating/joining a room, and testing a connection to the planned local WebSocket server at `ws://127.0.0.1:8765`.

**Live capture, local server implementation, WebRTC negotiation, and playback are not implemented yet.** The page labels these limitations rather than pretending a stream is already working.
