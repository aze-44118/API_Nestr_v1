import os
import datetime
import json
import xml.etree.ElementTree as ET
from Models.radio_assembler import generate_multivoice_podcast
from Supabase.supabase_client import get_client
from Supabase.supabase_storage_api import delete_file, download_file, upload_file

def send_podcast(user_id: str, podcast_text: str, first_name: str, user_token: str):

    supabase = get_client()

    try:
        # Convertir le texte JSON en Python
        script_json = json.loads(podcast_text)

        script_json = json.loads(podcast_text)
        audio_path = generate_multivoice_podcast(script_json, user_id)  
        
        audio_path = generate_multivoice_podcast(script_json, user_id)
      

        # ─── MODE TEST ───────────────────────────────────────────────────────────────
        # Commente cette ligne pour repasser en production
        # audio_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Static", "50b27131-0cb3-4813-a25b-89e2589f5388_podcast.mp3"))
        # ─── FIN MODE TEST ──────────────────────────────────────────────────────────

          
        # ─── MODE PROD ──────────────────────────────────────────────────────────────
        audio_path = generate_multivoice_podcast(podcast_text, user_id)
        # ─── FIN MODE PROD ──────────────────────────────────────────────────────────


        if not audio_path or not os.path.exists(audio_path):
            print("❌ Erreur : fichier audio non généré.")
            return False




        
        # Étape 2 – Upload vers Supabase Storage
        file_name = os.path.basename(audio_path)
        bucket_name = "podcast"  # Nom de ta bucket en minuscule
        storage_path = f"{user_id}/{file_name}"
        
        # Supprime ancien fichier audio si présent
        try:
            delete_file(bucket_name, storage_path, user_token)
            print(f"🗑️ Ancien fichier audio supprimé : {storage_path}")
        except Exception as e:
            print(f"ℹ️ Aucun MP3 à supprimer ou déjà supprimé : {e}")
            
        try:
            with open(audio_path, "rb") as f:
                upload_file(bucket_name, storage_path, f.read(), user_token, "audio/mpeg")
                print("✅ Fichier audio uploadé avec succès")
        except Exception as e:
            print(f"❌ Erreur lors de l'upload MP3 : {e}")
            return False


        
        # Étape 3 – Générer l'URL publique
        public_url = f"https://kgncwfrhnadiufdozxno.supabase.co/storage/v1/object/public/{bucket_name}/{storage_path}"

        # Étape 4 – Mise à jour du RSS par utilisateur
        from io import BytesIO  # en haut du fichier si pas encore là
        rss_file_name = "rss_feed.xml"
        rss_storage_path = f"rss/{user_id}/{rss_file_name}"

        # Si le RSS n'existe pas, on l'initialise avec un <rss><channel/>
        try:
            existing = download_file(bucket_name, rss_storage_path, user_token)
            tree = ET.ElementTree(ET.fromstring(existing))
        except Exception:
            rss = ET.Element("rss", version="2.0")
            ET.SubElement(rss, "channel")
            tree = ET.ElementTree(rss)

        root = tree.getroot()
        channel = root.find("channel")
        if channel is None:
            print("❌ Balise <channel> manquante.")
            return False

        rss_url = f"https://kgncwfrhnadiufdozxno.supabase.co/storage/v1/object/public/podcast/{rss_storage_path}"


        # Ajoute ou met à jour les métadonnées globales du podcast
        def set_or_update(elem_name, text):
            existing = channel.find(elem_name)
            if existing is not None:
                existing.text = text
            else:
                ET.SubElement(channel, elem_name).text = text

        set_or_update("title", f"{first_name}'s Briefing")
        set_or_update("description", "Le résumé de ta journée")
        set_or_update("language", "fr-FR")

        # Ajoute ou met à jour l'image
        image_tag = channel.find("image")
        if image_tag is None:
            image_tag = ET.SubElement(channel, "image")
            
        ET.SubElement(image_tag, "url").text = "https://kgncwfrhnadiufdozxno.supabase.co/storage/v1/object/public/podcast/podcast_cover_2.png"
        ET.SubElement(image_tag, "title").text = "Ton Podcast"
        ET.SubElement(image_tag, "link").text = rss_url





        # ➕ Création du nouvel épisode
        new_item = ET.Element("item")
        ET.SubElement(new_item, "title").text = f"{first_name}'s Briefing - {datetime.datetime.utcnow().strftime('%Y-%m-%d')}"
        ET.SubElement(new_item, "description").text = "Briefing personnalisé du jour."

        enclosure = ET.SubElement(new_item, "enclosure")
        enclosure.set("url", public_url)
        enclosure.set("type", "audio/mpeg")

        ET.SubElement(new_item, "pubDate").text = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
        ET.SubElement(new_item, "guid").text = f"{file_name}-{datetime.datetime.utcnow().isoformat()}"

        # ➕ Ajoute le nouvel épisode en haut
        channel.insert(0, new_item)

        # 🧹 Ne garde que les 10 plus récents
        existing_items = channel.findall("item")
        for old_item in existing_items[10:]:
            channel.remove(old_item)

        rss_io = BytesIO()
        tree.write(rss_io, encoding='utf-8', xml_declaration=True)
        rss_bytes = rss_io.getvalue()  # ✅ conserve bien ce que tu viens d’écrire

        # Supprime le fichier RSS s’il existe déjà
        try:
            delete_file(bucket_name, rss_storage_path, user_token)
            print(f"🗑️ Ancien fichier RSS supprimé : {rss_storage_path}")
        except Exception as e:
            print(f"ℹ️ Aucun RSS à supprimer ou déjà supprimé : {e}")

        try:
            upload_file(bucket_name, rss_storage_path, rss_bytes, user_token, "application/xml")
            print("✅ Fichier RSS uploadé avec succès")
        except Exception as e:
            print(f"❌ Erreur lors de l'upload RSS : {e}")
            return False



        rss_url = f"https://kgncwfrhnadiufdozxno.supabase.co/storage/v1/object/public/podcast/{rss_storage_path}"
        print(f"🔗 Lien RSS : {rss_url}")
        
        # Nettoyage du fichier temporaire
        os.remove(audio_path)

        print("✅ Podcast uploadé et RSS mis à jour avec succès 🎉")
        return rss_url

    except Exception as e:
        print(f"❌ [send_podcast] Erreur : {e}")
        return False

# git add . && git commit -m "Ton message" 
# && git push origin main

