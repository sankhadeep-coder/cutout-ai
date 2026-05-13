# CutOut.ai ✨

AI-powered background remover built with Python, Flask, and Rembg.

Remove image backgrounds instantly with multiple AI models, transparent/solid backgrounds, and built-in upscaling.

---

## Features

✅ AI background removal  
✅ 5 segmentation models  
✅ Transparent / White / Black background  
✅ Image upscaling (×2, ×3, ×4)  
✅ Drag & drop upload  
✅ Modern responsive UI  
✅ 100% private processing  

---

## Tech Stack

### Frontend
- HTML
- CSS
- JavaScript

### Backend
- Python
- Flask
- Rembg
- OpenCV
- Pillow

### Deployment
- Render

---

## Project Structure

cutout-ai/
├── app.py  
├── index.html  
├── requirements.txt  
├── render.yaml  
└── README.md  

---

## Run Locally

### Clone repository

git clone YOUR_REPOSITORY_URL

### Install dependencies

pip install -r requirements.txt

### Start server

python app.py

### Open app

Open index.html in your browser

---

## API Endpoint

### POST /remove-bg

Form data:

- image
- model
- bg
- upscale

---

## Supported Formats

JPG, PNG, WEBP, BMP, TIFF, GIF, AVIF

---

## Author

**Sankhadeep**

---

Made with ❤️ using AI + Python
