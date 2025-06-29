import os
from pathlib import Path
import streamlit as st
from werkzeug.utils import secure_filename

# Local Dev IP Override
DEV_MODE = st.sidebar.checkbox("Developer mode (override IP)", value=False)
if DEV_MODE:
    client_ip = st.sidebar.text_input("Simulate client IP", value="127.0.0.1")
else:
    # Replace this with your real IP‐fetching logic for production
    client_ip = "20.218.226.24"  # placeholder; swap for your get_client_ip()

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
    

