import streamlit as st
from PIL import Image
import os, random
from datetime import datetime

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="MiniFlix 🎬", layout="wide")
st.markdown(
    """
    <style>
        body {background-color: #141414; color: white;}
        h1, h2, h3, label, p {color: white !important;}
        .banner {text-align:center; padding:50px; border-radius:10px; 
                 background:linear-gradient(to right,#e50914,#b20710);}
        .section-title {font-size:24px; font-weight:bold; margin-top:30px;}
        .feedback-card {background:#1f1f1f; padding:15px; border-radius:10px; margin:10px 0;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------ SESSION STATE ------------------
if "watchlist" not in st.session_state:
    st.session_state.watchlist = []
if "feedback" not in st.session_state:
    st.session_state.feedback = []

# ------------------ SIDEBAR NAVIGATION ------------------
st.sidebar.title("🎬 MiniFlix")
page = st.sidebar.radio(
    "Navigate",
    ["🏠 Home", "🎞️ Library", "⭐ Trending", "📺 Watchlist", "💬 Feedback"],
)
image_folder = "images"
if not os.path.exists(image_folder):
    os.makedirs(image_folder)
all_images = [
    f for f in os.listdir(image_folder) if f.lower().endswith((".png", ".jpg", ".jpeg"))
]

# ===================================================
# HOME PAGE
# ===================================================
if page == "🏠 Home":
    st.markdown('<div class="banner"><h1>Welcome to MiniFlix</h1><p>Your Personal Movie Hub</p></div>', unsafe_allow_html=True)
    if not all_images:
        st.warning("Add some images to the 'images' folder!")
        st.stop()

    st.subheader("🔥 Featured Movies")
    cols = st.columns(5)
    for i, img in enumerate(random.sample(all_images, min(5, len(all_images)))):
        with cols[i]:
            st.image(os.path.join(image_folder, img), use_container_width=True)
            name = img.rsplit(".", 1)[0].replace("_", " ").title()
            st.caption(name)
            if img not in st.session_state.watchlist:
                if st.button("➕ Add", key=f"add_{i}"):
                    st.session_state.watchlist.append(img)
                    st.success("Added to Watchlist!")

# ===================================================
# LIBRARY PAGE
# ===================================================
elif page == "🎞️ Library":
    st.header("🎞️ My Library")
    uploaded = st.file_uploader("Upload Movie Poster", type=["png", "jpg", "jpeg"])
    if uploaded:
        path = os.path.join(image_folder, uploaded.name)
        with open(path, "wb") as f:
            f.write(uploaded.getbuffer())
        st.success("Movie Added!")
        st.rerun()

    st.subheader("All Movies")
    if not all_images:
        st.info("No movies found yet!")
    else:
        cols = st.columns(4)
        for i, img in enumerate(all_images):
            with cols[i % 4]:
                st.image(os.path.join(image_folder, img), use_container_width=True)
                st.caption(img.rsplit(".", 1)[0].replace("_", " ").title())
                if img not in st.session_state.watchlist:
                    if st.button("Add", key=f"add_lib_{i}"):
                        st.session_state.watchlist.append(img)
                        st.rerun()
                else:
                    st.caption("✅ In Watchlist")

# ===================================================
# TRENDING PAGE
# ===================================================
elif page == "⭐ Trending":
    st.header("⭐ Trending Now")
    if not all_images:
        st.info("No movies found!")
    else:
        trending = random.sample(all_images, min(8, len(all_images)))
        cols = st.columns(4)
        for i, img in enumerate(trending):
            with cols[i % 4]:
                st.image(os.path.join(image_folder, img), use_container_width=True)
                st.caption(f"#{i+1} {img.rsplit('.',1)[0].title()}")

# ===================================================
# WATCHLIST PAGE
# ===================================================
elif page == "📺 Watchlist":
    st.header("📺 My Watchlist")
    if not st.session_state.watchlist:
        st.info("Your watchlist is empty.")
    else:
        for img in st.session_state.watchlist:
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(os.path.join(image_folder, img), width=150)
            with col2:
                st.subheader(img.rsplit(".", 1)[0].replace("_", " ").title())
                if st.button("❌ Remove", key=f"remove_{img}"):
                    st.session_state.watchlist.remove(img)
                    st.rerun()

# ===================================================
# FEEDBACK PAGE
# ===================================================
elif page == "💬 Feedback":
    st.header("💬 Share Your Feedback")
    name = st.text_input("Your Name")
    rating = st.slider("Rate MiniFlix", 1, 5, 5)
    comment = st.text_area("Your Comments")
    if st.button("Submit"):
        if name and comment:
            st.session_state.feedback.append(
                {"name": name, "rating": rating, "comment": comment, "time": datetime.now().strftime("%H:%M:%S")}
            )
            st.success("Thanks for your feedback!")
        else:
            st.error("Please fill all fields!")

    st.markdown("---")
    if st.session_state.feedback:
        for fb in reversed(st.session_state.feedback):
            st.markdown(
                f"<div class='feedback-card'><b>{fb['name']}</b> ⭐{fb['rating']} <br>{fb['comment']} <br><i>{fb['time']}</i></div>",
                unsafe_allow_html=True,
            )
