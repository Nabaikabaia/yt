from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

CREATOR = {
    "name": "Nabees",
    "website": "https://nabees.online",
    "whatsapp_channel": "https://whatsapp.com/channel/0029VawtjOXJpe8X3j3NCZ3j"
}

# Home route
@app.route("/")
def home():
    return jsonify({
        "status": 200,
        "message": "Media Downloader API",
        "creator": CREATOR,
        "routes": {
            "youtube": "/api/ytdown?url=",
            "facebook": "/api/fb?id="
        }
    })


# =========================
# YouTube Downloader Route
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
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://ytdown.to",
        "Referer": "https://ytdown.to/",
        "User-Agent": "Mozilla/5.0",
        "X-Requested-With": "XMLHttpRequest"
    }

    payload = {
        "url": url
    }

    try:
        response = requests.post(endpoint, headers=headers, data=payload)
        data = response.json()

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
# Facebook Video Route
# =========================
@app.route("/api/fb", methods=["GET"])
def facebook():
    job_id = request.args.get("id")

    if not job_id:
        return jsonify({
            "status": 400,
            "error": "Missing job id"
        })

    url = f"https://app.publer.com/api/v1/job_status/{job_id}"

    headers = {
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers)
        data = response.json()

        video = None
        if data.get("payload"):
            video = data["payload"][0].get("path")

        return jsonify({
            "status": 200,
            "creator": CREATOR,
            "video": video,
            "raw": data
        })

    except Exception as e:
        return jsonify({
            "status": 500,
            "error": str(e)
        })


# Run server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
