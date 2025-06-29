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

## Environment Modes

The app uses a hard-coded `PROD` flag at the top of **`app.py`** to switch behavior:

* **Local Development** (`PROD = False`):

  * Shows **Dev Controls** in the sidebar to simulate any client IP (default `127.0.0.1`).
  * **No IP whitelist** enforced.

* **Production** (`PROD = True`):

  * Hides Dev Controls.
  * Attempts to detect the real public IP via query params, headers, or external services.
  * Only allows requests from the whitelisted IP (`20.218.226.24`).
  * Displays an “Access denied” message for other IPs.

To toggle, edit the top of **`app.py`**:

```python
# In local dev, set to False. In production, set to True.
PROD = False  # ← change to True before deploying
```

Then restart the app:

```bash
streamlit run app.py
```