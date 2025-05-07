# app.py
from flask import Flask
from flask_cors import CORS
from Route.briefing import briefing_bp
from Route.settings import settings_bp
import os

app = Flask(__name__)



# → Replace your simple CORS(app) with this:
CORS(app,
     resources={r"/api/*": {"origins": "*"}},
     supports_credentials=True,
     methods=["GET", "POST", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization"])


# Register blueprints
app.register_blueprint(briefing_bp)
app.register_blueprint(settings_bp)

# dans app.py, juste après app = Flask(__name__) et après register_blueprint(...)
print("=== Registered routes ===")
for rule in app.url_map.iter_rules():
    print(rule)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
