import os
from pathlib import Path
import streamlit as st
from werkzeug.utils import secure_filename
import requests

# Configuration
PROD = True  # Set to True in production
ALLOWED_IP = "20.218.226.24"
CACHE_TTL = 300  # seconds
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

# Helpers
@st.cache_data(ttl=CACHE_TTL)
def detect_public_ip():
    """Detect public IP via external services."""
    services = [
        'https://api.ipify.org?format=json',
        'https://httpbin.org/ip',
        'https://ipinfo.io/ip',
    ]
    for url in services:
        try:
            r = requests.get(url, timeout=3)
            if 'ipify' in url:
                return r.json().get('ip')
            if 'httpbin' in url:
                return r.json().get('origin', '').split(',')[0].strip()
            if 'ipinfo' in url:
                return r.text.strip()
        except requests.RequestException:
            continue
    return None


def check_ip_whitelist(prod: bool, allowed_ip: str) -> str:
    """Return the client IP after enforcing whitelist logic."""
    if not prod:
        st.sidebar.markdown("## Dev Controls")
        dev_mode = st.sidebar.checkbox("Developer mode", value=True)
        client_ip = st.sidebar.text_input("Simulated IP", value="127.0.0.1")
        return client_ip.strip()

    # Production: attempt auto-detection
    if 'client_ip' not in st.session_state:
        st.session_state.client_ip = None

    if st.session_state.client_ip is None:
        # Try query param
        params = st.experimental_get_query_params()
        ip_param = params.get("ip") or params.get("X-Forwarded-For")
        if ip_param:
            st.session_state.client_ip = ip_param[0].split(',')[0].strip()
        else:
            detected = detect_public_ip()
            if detected:
                st.session_state.client_ip = detected

    client_ip = st.session_state.client_ip or ""
    if client_ip != allowed_ip:
        st.error(f"🚫 Access denied: your IP ({client_ip}) is not allowed.")
        st.stop()
    return client_ip

# Main
client_ip = check_ip_whitelist(PROD, ALLOWED_IP)
st.set_page_config(page_title="Image Uploader", layout="wide")
st.title("🖼️ Image Uploader")

st.sidebar.markdown(f"**Current IP:** {client_ip}")
if PROD:
    st.sidebar.markdown(f"**Allowed IP:** {ALLOWED_IP}")

# Upload
uploaded = st.file_uploader("Choose an image to upload", type=list(ALLOWED_EXTENSIONS))
if uploaded:
    filename = secure_filename(uploaded.name)
    target = UPLOAD_DIR / filename
    with open(target, "wb") as f:
        f.write(uploaded.getbuffer())
    st.success(f"✅ '{filename}' uploaded.")

st.markdown("---")

# Display & Delete
st.subheader("Uploaded Images")
images = sorted(UPLOAD_DIR.iterdir())
if not images:
    st.info("No images uploaded yet.")
else:
    cols = st.columns(4)
    for idx, img in enumerate(images):
        with cols[idx % 4]:
            st.image(str(img), caption=img.name, use_column_width=True)
            if st.button(f"Delete {img.name}", key=img.name):
                img.unlink()
                st.experimental_rerun()
