import streamlit as st
import json

# Optional: bump up font size
st.markdown(
    """
    <style>
      html, body, [class*="css"] {
        font-size: 18px !important;
      }
      .pill {
        display: inline-block;
        background-color: #e0f3ff;
        color: #036fab;
        padding: 4px 10px;
        margin: 2px;
        border-radius: 10px;
        font-weight: 500;
      }
    </style>
    """,
    unsafe_allow_html=True
)

@st.cache_data
def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# Load data
topic_data = load_json("topic_data.json")       # [{id, words, posts}, ...]
comments_data = load_json("comments.json") # [{id, posts}, ...]

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Posts Explorer", "Comments Explorer"])

if page == "Posts Explorer":
    st.title("📂 Posts Explorer")
    # Select topic
    topic_ids = [t["id"] for t in topic_data]
    selected = st.sidebar.selectbox("Select Topic", topic_ids, key="posts_topic")
    topic = next(t for t in topic_data if t["id"] == selected)

    st.subheader(f"Topic {topic['id']} — Top 50 Words")
    # Display top words as styled pills
    pills_html = "".join(f"<span class='pill'>{w}</span>" for w in topic["words"])
    st.markdown(pills_html, unsafe_allow_html=True)

    st.subheader("Sampled 10 Posts")
    for post in topic["posts"]:
        st.markdown(f"- {post}")

else:  # Comments Explorer
    st.title("💬 Comments Explorer")
    comment_ids = [c["id"] for c in comments_data]
    selected = st.sidebar.selectbox("Select Topic", comment_ids, key="comments_topic")
    comment_group = next(c for c in comments_data if c["id"] == selected)

    st.subheader(f"Topic {comment_group['id']} — Top 50 Words")
    # Display top words as styled pills
    pills_html = "".join(f"<span class='pill'>{w}</span>" for w in comment_group["words"])
    st.markdown(pills_html, unsafe_allow_html=True)


    st.subheader(f"Topic {comment_group['id']} — Sampled 10 Comments")
    for comment in comment_group.get("posts", []):
        st.markdown(f"- {comment}")

