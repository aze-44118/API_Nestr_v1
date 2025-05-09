# Route/briefing.py
from flask import Blueprint, jsonify, request
from flask_cors import CORS, cross_origin
from Models.generator import generation_data
from Supabase.user_data import load_user_environment
from Models.mistral_client import nestr_briefing_courriel, nestr_briefing_script
from Output.email import send_email 
from Output.podcast import send_podcast
from Supabase.supabase_client import supabase
from Models.mistral_client import nestr_daily_mood
import traceback


briefing_bp = Blueprint(
    'briefing',
    __name__,
    url_prefix='/api/briefing'
)

# Applique le CORS automatiquement (GET + OPTIONS)
CORS(briefing_bp)

@briefing_bp.route(
    '',              # équivalent à /api/briefing
    methods=['GET'],
    strict_slashes=False
)
@cross_origin()     # permet CORS sur GET et OPTIONS
def generate_briefing():
    print("⚡️ generate_briefing called with args=", request.args)
    # ① Récupère l'user_id
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id manquant"}), 400

    # ② Vérifie le token Bearer
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return jsonify({"error": "token manquant"}), 401
    token = auth_header.split(" ", 1)[1]

    # ③ Vérifie la correspondance user/token
    try:
        user_data = supabase.auth.get_user(token)
        if user_data.user.id != user_id:
            return jsonify({"error": "user_id invalide"}), 403
    except Exception:
        return jsonify({"error": "token invalide"}), 401

    # ④ Charge l'environnement utilisateur (email, prénom, ville, etc.)
    user_env = load_user_environment(user_id)
    if user_env is None:
        print("   → user_env loaded:", user_env)
        return jsonify({"error": "profil introuvable"}), 404
    
    # ⑤ Récupère le first_name depuis la table user_env
    first_name = user_env.get("first_name")
    if not first_name:
        return jsonify({"error": "first_name introuvable"}), 500

    try:
        # ⑤ Génère le contenu brut
        data_brut = generation_data(user_id)




        # ⑥ Appel IA pour generation du texte 
        
        podcast_text = nestr_briefing_script(data_brut)
        if not isinstance(podcast_text, str):
            return jsonify({"error": "no response from Mistral Agent"}), 502
    
        '''
        email_text = nestr_briefing_courriel(data_brut)
        if not isinstance(email_text, str):
            return jsonify({"error": "no response from courriel agent"}), 502
        '''

        # 6.2 Appel IA pour analyse de donnees
        mood_json = nestr_daily_mood(data_brut)
        if not isinstance(mood_json, dict):
           return jsonify({"error": "no mood analysis response"}), 502


        # ⑦ Output email
        '''
        success = send_email(
            user_env.get("email", "aad.vergeron@gmail.com"),
            "Votre briefing du jour",
            email_text
        )
        if not success:
            return jsonify({"error": "failed to send email"}), 502
        '''
        
        # ⑦ Output podcast
        try:
            rss_url = send_podcast(
                user_id,
                podcast_text,
                first_name,
                token
            )

            if not rss_url:
                return jsonify({"error": "failed to send podcast"}), 502
        

        except Exception as e:
            import traceback
            print("🔥 Erreur dans send_podcast() :")
            traceback.print_exc()  # Affiche le détail de l'erreur dans les logs
            return jsonify({"error": f"Exception interne: {str(e)}"}), 500

        print("« Sans cesse la politesse exige, la bienséance ordonne ; sans cesse on suit des usages, jamais son propre génie. »")

        # ⑧ Tout est OK : 
        return jsonify({
            "status": "success",
            # "message": email_text,
            "raw": data_brut,
            "mood": mood_json,
            "html": rss_url,
            "podcast": podcast_text
        }), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
