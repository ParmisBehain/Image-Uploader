import os
from pathlib import Path
import streamlit as st
from werkzeug.utils import secure_filename

# Locally, don’t enforce the whitelist. On Cloud, enforce it.
PROD = True #It should be false for the local testing, so the local IP can see the website

if not PROD:
    # Local dev: sidebar toggle & simulate IP
    st.sidebar.markdown("## 🛠️ Dev Controls")
    DEV_MODE = st.sidebar.checkbox("Developer mode (override IP)", value=True)
    client_ip = st.sidebar.text_input("Simulated client IP", value="127.0.0.1")
else:
    # Production on Streamlit Cloud: grab real client IP from header
    client_ip = st.experimental_get_query_params().get("X-Forwarded-For", [""])[0]

# Whitelist logic only when PROD
if PROD:
    ALLOWED_IP = "138.246.3.8"
    if client_ip != ALLOWED_IP:
        st.error(f"🚫 Access denied: your IP ({client_ip}) is not allowed.")
        st.stop()

st.set_page_config(page_title="Image Uploader", layout="wide")
st.title("🖼️ Image Uploader")

# Ensure uploads directory exists
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

def allowed_file(filename: str) -> bool:
    EXT = {"png", "jpg", "jpeg", "gif"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in EXT

# Upload form
uploaded_file = st.file_uploader("Choose an image to upload", type=["png","jpg","jpeg","gif"])
if uploaded_file:
    fname = secure_filename(uploaded_file.name)
    save_path = UPLOAD_DIR / fname
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"✅ `{fname}` uploaded successfully.")

st.markdown("---")

# Display and delete existing images
st.subheader("Uploaded Images")
images = sorted(UPLOAD_DIR.iterdir())
if not images:
    st.info("No images uploaded yet.")
else:
    cols = st.columns(4)
    for idx, img_path in enumerate(images):
        with cols[idx % 4]:
            st.image(str(img_path), caption=img_path.name, use_column_width=True)
            if st.button(f"Delete `{img_path.name}`", key=img_path.name):
                img_path.unlink()
    

