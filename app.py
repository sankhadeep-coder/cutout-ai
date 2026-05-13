"""
CutOut.ai — Flask Backend (remove.bg API edition)
Lightweight: no rembg, no ONNX — runs fine on Render's free 512 MB tier.
"""

from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from PIL import Image
import requests as http_requests
import io, os

# ── config ─────────────────────────────────────────────────────────────────────
SUPPORTED     = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".tif", ".gif", ".avif"}
MAX_FILE_MB   = 20
MAX_BYTES     = MAX_FILE_MB * 1024 * 1024
REMOVE_BG_URL = "https://api.remove.bg/v1.0/removebg"
API_KEY       = os.environ.get("REMOVE_BG_API_KEY", "u5bvxwgA7owFdNSmvxA9g31S")

app = Flask(__name__)
CORS(app)

# ── helpers ────────────────────────────────────────────────────────────────────
def apply_background(png_bytes: bytes, bg_mode: str) -> bytes:
    """Composite a solid colour behind the transparent cutout PNG."""
    if bg_mode not in ("white", "black"):
        return png_bytes  # keep transparent

    img    = Image.open(io.BytesIO(png_bytes)).convert("RGBA")
    colour = (255, 255, 255, 255) if bg_mode == "white" else (0, 0, 0, 255)
    bg     = Image.new("RGBA", img.size, colour)
    bg.paste(img, mask=img.split()[3])

    buf = io.BytesIO()
    bg.save(buf, format="PNG", optimize=True)
    buf.seek(0)
    return buf.read()

# ── routes ─────────────────────────────────────────────────────────────────────
@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "CutOut.ai backend running", "version": "2.0"})


@app.route("/remove-bg", methods=["POST"])
def remove_bg():
    # ── validate file ──────────────────────────────────────────────────────────
    if "image" not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in SUPPORTED:
        return jsonify({"error": f"Unsupported format: {ext}"}), 400

    file_bytes = file.read()
    if len(file_bytes) > MAX_BYTES:
        return jsonify({"error": f"File too large (max {MAX_FILE_MB} MB)"}), 413

    # ── parse options ──────────────────────────────────────────────────────────
    bg_mode = request.form.get("bg", "transparent")
    if bg_mode not in ("transparent", "white", "black"):
        bg_mode = "transparent"

    upscale  = request.form.get("upscale", "1")
    size_map = {"1": "regular", "2": "hd", "3": "4k", "4": "4k"}
    size     = size_map.get(upscale, "regular")

    # ── call remove.bg ─────────────────────────────────────────────────────────
    try:
        resp = http_requests.post(
            REMOVE_BG_URL,
            files   ={"image_file": (file.filename, file_bytes, file.content_type)},
            data    ={"size": size},
            headers ={"X-Api-Key": API_KEY},
            timeout =60,
        )

        if resp.status_code == 402:
            return jsonify({"error": "remove.bg monthly quota exhausted. Visit remove.bg to top up."}), 402

        if resp.status_code != 200:
            try:
                detail = resp.json().get("errors", [{}])[0].get("title", resp.text)
            except Exception:
                detail = resp.text[:200]
            return jsonify({"error": f"remove.bg error: {detail}"}), resp.status_code

        png_bytes = resp.content

    except http_requests.exceptions.Timeout:
        return jsonify({"error": "remove.bg timed out — try a smaller image."}), 504
    except http_requests.exceptions.RequestException as exc:
        return jsonify({"error": f"Network error: {exc}"}), 503

    # ── apply background if requested ──────────────────────────────────────────
    try:
        final_bytes = apply_background(png_bytes, bg_mode)
    except Exception as exc:
        return jsonify({"error": f"Post-processing failed: {exc}"}), 500

    return send_file(
        io.BytesIO(final_bytes),
        mimetype      ="image/png",
        as_attachment =False,
        download_name ="cutout_result.png",
    )


# ── run ────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n✦ CutOut.ai backend (remove.bg edition)")
    print("  → http://localhost:5000\n")
    app.run(host="0.0.0.0", port=5000, debug=False)
