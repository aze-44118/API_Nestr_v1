import os
import requests

SUPABASE_URL = os.getenv("SUPABASE_URL")

def upload_file(bucket: str, path: str, file_bytes: bytes, token: str, content_type="application/octet-stream"):
    url = f"{SUPABASE_URL}/storage/v1/object/{bucket}/{path}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": content_type
    }
    response = requests.post(url, headers=headers, data=file_bytes)
    if response.status_code not in (200, 201):
        raise Exception(f"Upload failed: {response.status_code} - {response.text}")
    return response

def delete_file(bucket: str, path: str, token: str):
    url = f"{SUPABASE_URL}/storage/v1/object/{bucket}/{path}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.delete(url, headers=headers)
    if response.status_code not in (200, 204):
        raise Exception(f"Delete failed: {response.status_code} - {response.text}")
    return response

def download_file(bucket: str, path: str, token: str) -> bytes:
    url = f"{SUPABASE_URL}/storage/v1/object/{bucket}/{path}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Download failed: {response.status_code} - {response.text}")
    return response.content
