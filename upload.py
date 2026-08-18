import sys
import requests

def upload_file(file_path):
    url = "https://paste.rs"
    with open(file_path, "rb") as f:
        resp = requests.put(url, data=f)
    if resp.status_code == 200:
        print("Upload successful! URL:", resp.text.strip())
    else:
        print("Upload failed:", resp.status_code, resp.text)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python upload.py <file_path>")
        sys.exit(1)
    upload_file(sys.argv[1])