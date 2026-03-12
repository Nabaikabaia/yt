from flask import Flask, request, jsonify
import requests
import time

app = Flask(__name__)

CREATOR = {
    "name": "Nabees",
    "website": "https://nabees.online",
    "whatsapp_channel": "https://whatsapp.com/channel/0029VawtjOXJpe8X3j3NCZ3j"
}

# ========================
# Home Route
# ========================
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


# ========================
# YouTube Downloader
# ========================
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


# ========================
# Facebook Downloader
# ========================
@app.route("/api/fb", methods=["GET"])
def fb_downloader():
    url = request.args.get("url")

    if not url:
        return jsonify({
            "status": 400,
            "error": "Missing Facebook URL"
        })

    try:
        # Step 1: Create job
        create_job_url = "https://app.publer.com/api/v1/media"

        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        }

        payload = {
            "url": url
        }

        job = requests.post(create_job_url, json=payload, headers=headers)
        job_data = job.json()

        job_id = job_data.get("id")

        if not job_id:
            return jsonify({
                "status": 500,
                "error": "Failed to create job",
                "response": job_data
            })

        # Step 2: Wait a bit for processing
        time.sleep(3)

        # Step 3: Get job result
        status_url = f"https://app.publer.com/api/v1/job_status/{job_id}"

        r = requests.get(status_url, headers=headers)
        data = r.json()

        if "payload" not in data:
            return jsonify({
                "status": 202,
                "message": "Video still processing",
                "response": data
            })

        video = data["payload"][0]["path"]

        return jsonify({
            "status": 200,
            "creator": CREATOR,
            "video": video
        })

    except Exception as e:
        return jsonify({
            "status": 500,
            "error": str(e)
        })


# ========================
# Run API
# ========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
