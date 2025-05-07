import requests
from Config.config import BREVO_API_KEY

BREVO_URL = "https://api.brevo.com/v3/smtp/email"

def send_email(to: str, subject: str, body: str) -> bool:
    """
    Envoie un email HTML via l’API SMTP de Brevo.

    :param to: adresse email du destinataire
    :param subject: sujet de l’email
    :param body: contenu HTML de l’email
    :return: True si l’email a été envoyé avec succès, False sinon
    """
    # Debug
    print(f"[send_email] to: {to}")
    print(f"[send_email] subject: {subject}")
    print(f"[send_email] body: {body[:100]}...")  # preview only

    payload = {
        "sender": {
            "name": "Nestr Assistant",
            "email": "aad.vergeron@gmail.com"
        },
        "to": [{"email": to}],
        "subject": subject,
        "htmlContent": body
    }

    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json"
    }

    try:
        resp = requests.post(BREVO_URL, json=payload, headers=headers)
        if resp.status_code in (200, 201, 202):
            print(f"✅ Email successfully sent to {to}")
            return True
        else:
            print(f"❌ Brevo error ({resp.status_code}): {resp.text}")
            return False
    except Exception as e:
        print(f"❌ Exception sending email: {e}")
        return False
