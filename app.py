from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

CREATOR = {
    "name": "Nabees",
    "website": "https://nabees.online",
    "whatsapp_channel": "https://whatsapp.com/channel/0029VawtjOXJpe8X3j3NCZ3j"
}

@app.route("/")
def home():
    return jsonify({
        "status": 200,
        "message": "YouTube Downloader API",
        "creator": CREATOR
    })

@app.route("/api/ytdown", methods=["GET"])
def ytdown():
    url = request.args.get("url")

    if not url:
        return jsonify({
            "status": 400,
            "error": "Provide a YouTube URL"
        })

    endpoint = "https://app.ytdown.to/proxy.php"

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://ytdown.to",
        "Referer": "https://ytdown.to/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }

    payload = {
        "url": url
    }

    try:
        response = requests.post(endpoint, headers=headers, data=payload, timeout=30)
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
