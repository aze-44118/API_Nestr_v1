from flask import Blueprint, request, jsonify
import sqlite3

settings_bp = Blueprint('settings', __name__, url_prefix='/api/settings')

@settings_bp.route('/update', methods=['POST'])
def update_settings():
    try:
        data = request.get_json()

        first_name = data.get('first_name')
        weather = data.get('weather')
        news = data.get('news')

        # Vérification que les champs sont présents
        if first_name is None or weather is None or news is None:
            return jsonify({"error": "Missing fields in request."}), 400

        try:
            weather = int(weather)
            news = int(news)
        except ValueError:
            return jsonify({"error": "Weather and News must be integers (0 or 1)."}), 400

        db_path = os.path.join(os.path.dirname(__file__), '..', 'Static', 'user_profile.db')
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            UPDATE user_profile
            SET first_name = ?, weather = ?, news = ?
            WHERE id = 1
            """, (first_name, weather, news))
            conn.commit()

        return jsonify({"message": "Profile updated successfully."})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500