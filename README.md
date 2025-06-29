# Image Uploader

A simple Streamlit web application that lets users **upload** and **delete** images, with access restricted to a single VPN IP address (`20.218.226.24`). Includes a “Developer mode” override for local testing.

---

## Features

* **Upload** PNG, JPG, JPEG & GIF images
* **Delete** previously uploaded images
* **IP Whitelisting** – only requests from `20.218.226.24` are allowed in production
* **Developer Mode** sidebar toggle to simulate arbitrary IPs (for local testing)

---

## Project Structure

```
Image Uploader/
├─ .gitignore            # ignore .venv/, uploads/, __pycache__, etc.
├─ README.md             # this file
├─ requirements.txt      # Python dependencies
├─ app.py                # Streamlit application with upload/delete & IP logic
└─ uploads/              # (empty) directory where images are saved at runtime
```

---

## Installation & Local Development

1. **Clone the repo**

   ```bash
   git clone https://github.com/ParmisBehain/Image-Uploader.git
   cd image-uploader
   ```

2. **Create & activate a virtual environment**

   ```bash
   python -m venv .venv
   # Windows (PowerShell):
   .\.venv\Scripts\Activate.ps1
   # macOS/Linux (bash):
   source .venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**

   ```bash
   streamlit run app.py
   ```

5. **Open** your browser at `http://localhost:8501`

---

## Deployment

You can deploy on any Python-compatible host:

* **Streamlit Community Cloud**
* **Heroku** (add a `Procfile`: `web: streamlit run app.py --server.port $PORT`)
* **DigitalOcean App Platform**, **AWS**, **GCP**, etc.

1. Push your code to GitHub.
2. Connect your repo on the deploy platform.
3. Configure your start command:

   ```bash
   streamlit run app.py
   ```
4. Ensure the real client IP is forwarded to the app so whitelisting works.

---

## Environment Modes

The app uses a hard-coded `PROD` flag in **`app.py`** to switch between:

- **Local Development** (`PROD = False`)  
  - A **Dev Controls** sidebar appears, letting you toggle “Developer mode” and simulate any client IP (default `127.0.0.1`).  
  - No real IP-whitelist is enforced so you can freely test upload/delete functionality locally.

- **Production** (`PROD = True`)  
  - Sidebar controls are hidden.  
  - The app reads the actual client IP from the `X-Forwarded-For` header and only allows requests from `20.218.226.24`.  
  - All other IPs see an “Access denied” message.

### How to Toggle

1. Open **`app.py`** in your editor.  
2. At the very top, set the flag:

   ```python
   # In local dev, set to False. In production, set to True.
   PROD = False    # ← change to True before you deploy
