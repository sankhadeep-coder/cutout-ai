# ✦ CutOut.ai — AI Background Remover

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Flask-3.x-black?style=for-the-badge&logo=flask&logoColor=white"/>
  <img src="https://img.shields.io/badge/remove.bg-API-00D4AA?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Render-Deployed-7C6FFF?style=for-the-badge&logo=render&logoColor=white"/>
  <img src="https://img.shields.io/badge/Free_Tier-512MB_Safe-brightgreen?style=for-the-badge"/>
</p>

<p align="center">
  Remove image backgrounds instantly with AI — no Photoshop, no manual selection, no BS.
</p>

---

## 🌐 Live Demo

> **[cutout-ai.onrender.com](https://cutout-ai.onrender.com)**

---

## 📸 What It Does

Upload any image and CutOut.ai removes the background in seconds using the **remove.bg API**. Supports transparent, white, or black output backgrounds, multiple quality levels, and a wide range of image formats.

---

## ✨ Features

| Feature | Details |
|---|---|
| 🤖 AI-Powered | Powered by remove.bg's state-of-the-art background removal API |
| 🖼️ Format Support | JPG, PNG, WEBP, BMP, TIFF, GIF, AVIF — up to 20 MB |
| 🎨 Background Modes | Transparent, White, or Black output |
| 📐 Quality Levels | Regular → HD → 4K output via upscale selector |
| ⚡ Fast | Results in seconds, no heavy ML model loaded on server |
| 🔒 Lightweight | Runs comfortably within Render's free 512 MB RAM tier |
| 🌍 Fully Hosted | Frontend + backend served from a single Flask app |

---

## 🏗️ Tech Stack

- **Frontend** — Vanilla HTML/CSS/JS (single `index.html`, no framework)
- **Backend** — Python + Flask
- **Background Removal** — [remove.bg REST API](https://www.remove.bg/api)
- **Image Post-processing** — Pillow (background compositing)
- **Hosting** — [Render](https://render.com) (free tier)

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- A free [remove.bg API key](https://www.remove.bg/api) (50 images/month free, no credit card)

### Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/your-username/cutout-ai.git
cd cutout-ai

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your API key (or it uses the hardcoded default)
export REMOVE_BG_API_KEY=your_api_key_here

# 4. Start the server
python app.py
```

Then open **http://localhost:5000** in your browser.

---

## ☁️ Deploy to Render (Free)

1. Push this repo to GitHub
2. Go to [render.com](https://render.com) → **New Web Service** → connect your repo
3. Render auto-detects `render.yaml` — no manual config needed
4. *(Optional)* Add `REMOVE_BG_API_KEY` in **Environment** settings to override the default key
5. Hit **Deploy** — your app will be live at `https://your-service-name.onrender.com`

> **Note:** Free Render instances spin down after inactivity. First request after sleep may take ~30 seconds to wake up.

---

## 📁 Project Structure

```
cutout-ai/
├── app.py            # Flask backend — serves UI + handles /remove-bg API
├── index.html        # Frontend UI (drag-drop, preview, settings)
├── requirements.txt  # Python dependencies (lightweight — no ML libs)
└── render.yaml       # Render deployment config
```

---

## 🔌 API Reference

### `POST /remove-bg`

Removes the background from an uploaded image.

**Form Data**

| Field | Type | Required | Description |
|---|---|---|---|
| `image` | file | ✅ | Image file (JPG, PNG, WEBP, etc.) |
| `bg` | string | ❌ | Output background: `transparent` (default), `white`, `black` |
| `upscale` | string | ❌ | Quality: `1` = Regular, `2` = HD, `3`/`4` = 4K |

**Response**

Returns a `image/png` file on success, or a JSON error object on failure.

```json
// Error example
{ "error": "remove.bg monthly quota exhausted. Visit remove.bg to top up." }
```

---

## ⚙️ Environment Variables

| Variable | Required | Description |
|---|---|---|
| `REMOVE_BG_API_KEY` | Optional | Your remove.bg API key. Falls back to hardcoded default if not set. |

---

## 📦 Dependencies

```
flask
flask-cors
Pillow
requests
gunicorn
```

No ONNX, no rembg, no OpenCV — installs in seconds and uses ~50 MB RAM.

---

## 🙋 FAQ

**Why not use `rembg` locally?**
`rembg` + ONNX runtime consume 400–600 MB at import time alone, which instantly crashes Render's free 512 MB instances. The remove.bg API delivers equal or better quality with near-zero server memory usage.

**Is my data private?**
Images are sent to remove.bg for processing and are subject to their [privacy policy](https://www.remove.bg/privacy). They are not stored by this app.

**What happens when the free quota runs out?**
You'll see a clear error message: *"remove.bg monthly quota exhausted."* Get a new key or upgrade at [remove.bg](https://www.remove.bg).

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

<p align="center">
  Made with ♥ by <strong>Sankhadeep</strong> &nbsp;·&nbsp; Powered by remove.bg · Flask · Python
</p>
