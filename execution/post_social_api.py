import sys
import json
import os
import requests
import base64
from dotenv import load_dotenv

load_dotenv("d:/AntiGravity/projeto_01/execution/.env")

META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
META_PAGE_ID = os.getenv("META_PAGE_ID")
INSTAGRAM_ACCOUNT_ID = os.getenv("INSTAGRAM_ACCOUNT_ID")

def post_to_facebook(message, image_url):
    if not META_ACCESS_TOKEN or not META_PAGE_ID:
        return {"status": "error", "message": "Missing credentials"}
    if image_url:
        url = f"https://graph.facebook.com/v19.0/{META_PAGE_ID}/photos"
        data = {"message": message, "url": image_url, "access_token": META_ACCESS_TOKEN}
    else:
        url = f"https://graph.facebook.com/v19.0/{META_PAGE_ID}/feed"
        data = {"message": message, "access_token": META_ACCESS_TOKEN}
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"status": "error", "details": str(e)}

def post_to_instagram(caption, image_url):
    if not META_ACCESS_TOKEN or not INSTAGRAM_ACCOUNT_ID:
        return {"status": "error", "message": "Missing credentials"}
    if not image_url:
        return {"status": "error", "message": "Instagram requires an image"}
    media_url = f"https://graph.facebook.com/v19.0/{INSTAGRAM_ACCOUNT_ID}/media"
    media_data = {"image_url": image_url, "caption": caption, "access_token": META_ACCESS_TOKEN}
    try:
        container_res = requests.post(media_url, data=media_data)
        container_res.raise_for_status()
        creation_id = container_res.json().get("id")
        publish_url = f"https://graph.facebook.com/v19.0/{INSTAGRAM_ACCOUNT_ID}/media_publish"
        publish_data = {"creation_id": creation_id, "access_token": META_ACCESS_TOKEN}
        publish_res = requests.post(publish_url, data=publish_data)
        publish_res.raise_for_status()
        return publish_res.json()
    except Exception as e:
        return {"status": "error", "details": str(e)}

if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            input_data = base64.b64decode(sys.argv[1]).decode('utf-8')
        else:
            input_data = sys.stdin.read()
        data = json.loads(input_data)
        message_fb = data.get("legenda_facebook", "")
        message_ig = data.get("legenda_instagram", "")
        image_url = data.get("image_url", "")
        
        fb_result = post_to_facebook(message_fb, image_url)
        ig_result = post_to_instagram(message_ig, image_url)
        
        print(json.dumps({"facebook": fb_result, "instagram": ig_result}))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
