import urllib.request
import json

KEY = "e8b1d9c4f72a4e5bb09c614d3f1a8e2b"
HOST = "ultimatethumbnailmaker.pages.dev"
KEY_LOCATION = f"https://{HOST}/{KEY}.txt"

URLS = [
    f"https://{HOST}/",
    f"https://{HOST}/youtube-thumbnail-maker/",
    f"https://{HOST}/gaming-thumbnail-maker/",
    f"https://{HOST}/thumbnail-maker-with-background-removal/",
    f"https://{HOST}/how-to-make-a-youtube-thumbnail/",
    f"https://{HOST}/about/",
    f"https://{HOST}/contact/",
    f"https://{HOST}/privacy-policy/"
]

payload = {
    "host": HOST,
    "key": KEY,
    "keyLocation": KEY_LOCATION,
    "urlList": URLS
}

data = json.dumps(payload).encode("utf-8")
req = urllib.request.Request(
    "https://api.indexnow.org/indexnow",
    data=data,
    headers={
        "Content-Type": "application/json; charset=utf-8",
        "User-Agent": "IndexNow-Submitter/1.0"
    }
)

try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        print(f"IndexNow API response status: {resp.status}")
except urllib.error.HTTPError as e:
    print(f"IndexNow API HTTP response: {e.code} - {e.read().decode('utf-8')}")
except Exception as e:
    print(f"IndexNow submission error: {e}")
