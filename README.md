# Shot Counter

A minimal Flask webapp to track how many shots each player has had. Everyone can add players and increment any player's count.

## Running locally

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then open [http://localhost:5000](http://localhost:5000) in your browser.

## Deploying

This app only requires Python and a few dependencies, making it easy to host on platforms like Heroku, Fly.io, or any service that can run a Flask application. Ensure the working directory is writable so SQLite can store `shots.db`.
