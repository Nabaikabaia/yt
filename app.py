from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

CREATOR = {
    "name": "Nabees",
    "website": "https://nabees.online",
    "whatsapp_channel": "https://whatsapp.com/channel/0029VawtjOXJpe8X3j3NCZ3j"
}

# =========================
# BEAUTIFUL HOMEPAGE
# =========================
@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html>
<head>
<title>Nabees Media API</title>
<style>

body{
background:#0f172a;
font-family:Arial, sans-serif;
color:white;
text-align:center;
padding:50px;
}

.container{
max-width:800px;
margin:auto;
background:#111827;
padding:40px;
border-radius:12px;
box-shadow:0 0 30px rgba(0,255,150,0.2);
}

h1{
color:#00ff9d;
font-size:40px;
margin-bottom:10px;
}

.creator{
color:#38bdf8;
margin-bottom:30px;
}

.endpoint{
display:block;
background:#1f2937;
padding:15px;
margin:10px 0;
border-radius:8px;
text-decoration:none;
color:#00ff9d;
font-weight:bold;
transition:0.3s;
}

.endpoint:hover{
background:#00ff9d;
color:black;
transform:scale(1.05);
}

.footer{
margin-top:30px;
color:#9ca3af;
font-size:14px;
}

</style>
</head>

<body>

<div class="container">

<h1>🚀 Media Downloader API</h1>

<div class="creator">
Created by <b>Nabees</b>
</div>

<h3>Available Endpoints</h3>

<a class="endpoint" href="/api/ytdown?url=">
YouTube Downloader
</a>

<a class="endpoint" href="/api/fb?url=">
Facebook Downloader
</a>

<a class="endpoint" href="/api/tiktok?url=">
TikTok Downloader
</a>

<a class="endpoint" href="/api/ig?url=">
Instagram Downloader
</a>

<div class="footer">
API Service • nabees.online
</div>

</div>

</body>
</html>
"""

# =========================
# YOUTUBE DOWNLOADER
# =========================
@app.route("/api/ytdown", methods=["GET"])
def ytdown():
    url = request.args.get("url")
    if not url:
        return jsonify({"status": 400, "error": "Missing YouTube URL"})

    endpoint = "https://app.ytdown.to/proxy.php"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://ytdown.to",
        "Referer": "https://ytdown.to/",
        "X-Requested-With": "XMLHttpRequest"
    }
    payload = {"url": url}

    try:
        r = requests.post(endpoint, headers=headers, data=payload)
        data = r.json()
        return jsonify({"status": 200, "creator": CREATOR, "result": data})
    except Exception as e:
        return jsonify({"status": 500, "error": str(e)})


# =========================
# FACEBOOK DOWNLOADER
# =========================
@app.route("/api/fb", methods=["GET"])
def fb():
    url = request.args.get("url")
    if not url:
        return jsonify({"status": 400, "error": "Missing Facebook URL"})

    api = f"https://apiskeith.vercel.app/download/fbdown?url={url}"
    headers = {"Accept": "application/json", "Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}

    try:
        r = requests.get(api, headers=headers)
        data = r.json()
        return jsonify({"status": 200, "creator": CREATOR, "data": data.get("result")})
    except Exception as e:
        return jsonify({"status": 500, "error": str(e)})


# =========================
# TIKTOK DOWNLOADER
# =========================
@app.route("/api/tiktok", methods=["GET"])
def tiktok():
    url = request.args.get("url")
    if not url:
        return jsonify({"status": 400, "error": "Missing TikTok URL"})

    api = f"https://api.bk9.dev/download/tiktok3?url={url}"
    headers = {"Accept": "application/json", "Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}

    try:
        r = requests.get(api, headers=headers)
        data = r.json()
        return jsonify({"status": 200, "creator": CREATOR, "data": data.get("BK9")})
    except Exception as e:
        return jsonify({"status": 500, "error": str(e)})


# =========================
# INSTAGRAM DOWNLOADER
# =========================
@app.route("/api/ig", methods=["GET"])
def instagram():
    url = request.args.get("url")
    if not url:
        return jsonify({"status": 400, "error": "Missing Instagram URL"})

    api = f"https://api.bk9.dev/download/instagram2?url={url}"
    headers = {"Accept": "application/json", "Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}

    try:
        r = requests.get(api, headers=headers)
        data = r.json()
        return jsonify({"status": 200, "creator": CREATOR, "data": data.get("BK9")})
    except Exception as e:
        return jsonify({"status": 500, "error": str(e)})


# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
