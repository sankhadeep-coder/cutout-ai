"""
CutOut.ai — Flask Backend
Run: python app.py
API: POST /remove-bg
"""

from flask import Flask, request, send_file, jsonify, send_from_directory
from flask_cors import CORS
from rembg import remove, new_session
from PIL import Image
import cv2, numpy as np, io, os, sys, subprocess

# ── auto-install deps ──────────────────────────────────────────────────────────
REQUIRED = ["flask", "flask-cors", "rembg[cpu]", "Pillow", "opencv-python-headless"]

def install_deps():
    for pkg in REQUIRED:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", pkg])

try:
    from flask import Flask
    from flask_cors import CORS
    from rembg import remove, new_session
    from PIL import Image
    import cv2, numpy as np
except ImportError:
    print("Installing required packages, please wait...")
    install_deps()
    from flask import Flask
    from flask_cors import CORS
    from rembg import remove, new_session
    from PIL import Image
    import cv2, numpy as np

# ── config ─────────────────────────────────────────────────────────────────────
SUPPORTED = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".tif", ".gif", ".avif"}
MAX_FILE_MB = 20
MAX_BYTES = MAX_FILE_MB * 1024 * 1024

MODELS = [
    "isnet-general-use",
    "u2net_human_seg",
    "u2net",
    "silueta",
    "u2netp",
]

app = Flask(__name__)
CORS(app)  # allow requests from your HTML frontend

# ── helpers ────────────────────────────────────────────────────────────────────
def process_image(
    img: Image.Image,
    model: str = "isnet-general-use",
    upscale: int = 1,
    bg_mode: str = "transparent"
) -> Image.Image:
    img = img.convert("RGBA")
    session = new_session(model)
    result = remove(img, session=session).convert("RGBA")

    if upscale > 1:
        arr = np.array(result)
        h, w = arr.shape[:2]
        arr = cv2.resize(arr, (w * upscale, h * upscale), interpolation=cv2.INTER_LANCZOS4)
        result = Image.fromarray(arr, "RGBA")

    if bg_mode == "white":
        bg = Image.new("RGBA", result.size, (255, 255, 255, 255))
        bg.paste(result, mask=result.split()[3])
        return bg
    elif bg_mode == "black":
        bg = Image.new("RGBA", result.size, (0, 0, 0, 255))
        bg.paste(result, mask=result.split()[3])
        return bg

    return result  # transparent

# ── routes ─────────────────────────────────────────────────────────────────────
@app.route("/", methods=["GET"])
def home():
    return send_from_directory(".", "index.html")


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
        return jsonify({"error": f"File too large (max {MAX_FILE_MB}MB)"}), 413

    # ── parse options ──────────────────────────────────────────────────────────
    model   = request.form.get("model", "isnet-general-use")
    bg_mode = request.form.get("bg", "transparent")
    upscale = int(request.form.get("upscale", 1))

    if model not in MODELS:
        model = "isnet-general-use"
    if bg_mode not in ("transparent", "white", "black"):
        bg_mode = "transparent"
    upscale = max(1, min(upscale, 4))

    # ── process ────────────────────────────────────────────────────────────────
    try:
        img = Image.open(io.BytesIO(file_bytes))

        # handle animated GIFs — use first frame only
        if getattr(img, "is_animated", False):
            img.seek(0)

        result = process_image(img, model=model, upscale=upscale, bg_mode=bg_mode)

        # return as PNG
        buf = io.BytesIO()
        result.save(buf, format="PNG", optimize=True)
        buf.seek(0)

        return send_file(
            buf,
            mimetype="image/png",
            as_attachment=False,
            download_name="cutout_result.png"
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── run ────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n✦ CutOut.ai backend starting...")
    print("  → API running at: http://localhost:5000")
    print("  → Open index.html in your browser\n")
    port = int(os.environ.get("PORT", 5000)) 
    app.run(host="0.0.0.0", port=port, debug=False)
