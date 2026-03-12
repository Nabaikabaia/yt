from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

CREATOR = {
    "name": "Nabees",
    "website": "https://nabees.online",
    "whatsapp_channel": "https://whatsapp.com/channel/0029VawtjOXJpe8X3j3NCZ3j"
}

# =========================
# HOME
# =========================
@app.route("/")
def home():
    return jsonify({
        "status": 200,
        "message": "Media Downloader API",
        "creator": CREATOR,
        "routes": {
            "youtube": "/api/ytdown?url=",
            "facebook": "/api/fb?url="
        }
    })


# =========================
# YOUTUBE DOWNLOADER
# =========================
@app.route("/api/ytdown", methods=["GET"])
def ytdown():

    url = request.args.get("url")

    if not url:
        return jsonify({
            "status": 400,
            "error": "Missing YouTube URL"
        })

    endpoint = "https://app.ytdown.to/proxy.php"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://ytdown.to",
        "Referer": "https://ytdown.to/",
        "X-Requested-With": "XMLHttpRequest"
    }

    payload = {
        "url": url
    }

    try:
        r = requests.post(endpoint, headers=headers, data=payload)
        data = r.json()

        return jsonify({
            "status": 200,
            "creator": CREATOR,
            "result": data
        })

    except Exception as e:
        return jsonify({
            "status": 500,
            "error": str(e)
        })


# =========================
# FACEBOOK DOWNLOADER
# =========================
@app.route("/api/fb", methods=["GET"])
def fb():

    url = request.args.get("url")

    if not url:
        return jsonify({
            "status": 400,
            "error": "Missing Facebook URL"
        })

    try:

        # follow redirect for share links
        r = requests.get(url, allow_redirects=True, headers={
            "User-Agent": "Mozilla/5.0"
        })

        real_url = r.url

        api = f"https://api.fdownloader.net/api/ajaxSearch?url={real_url}"

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json"
        }

        res = requests.get(api, headers=headers)

        data = res.json()

        return jsonify({
            "status": 200,
            "creator": CREATOR,
            "video_data": data
        })

    except Exception as e:
        return jsonify({
            "status": 500,
            "error": str(e)
        })


# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
