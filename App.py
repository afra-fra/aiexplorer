import streamlit as st
import json
import re

# --- CSS styling ---
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
      mark {
        background-color: #fff59d;
        padding: 0 2px;
        border-radius: 3px;
      }
    </style>
    """,
    unsafe_allow_html=True
)

# Security question styling
st.markdown(
    """
    <style>
      .security-text {
         font-size: 28px !important;
      }
    </style>
    """,
    unsafe_allow_html=True
)

# Define security question
security_question = "What’s the key to success?"
security_answer = "luck"

# Authentication state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown('<p class="security-text">Please answer the security question to access this web:</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="security-text"><strong>{security_question}</strong></p>', unsafe_allow_html=True)
    user_answer = st.text_input("Your Answer:")
    if user_answer and user_answer.strip().lower() == security_answer:
        st.session_state.authenticated = True
    elif user_answer:
        st.error("Incorrect answer. Please try again.")

if not st.session_state.authenticated:
    st.stop()

@st.cache_data
def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# Highlighting function
def highlight_text(text, words):
    # Sort by length to match longer phrases first
    for w in sorted(words, key=len, reverse=True):
        pattern = re.compile(rf"\b({re.escape(w)})\b", flags=re.IGNORECASE)
        text = pattern.sub(r"<mark>\1</mark>", text)
    return text

# Load data
topic_data = load_json("topic_data.json")
comments_data = load_json("comments.json")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Posts Explorer", "Comments Explorer"])

# --- Posts Explorer ---
if page == "Posts Explorer":
    st.title("📂 Posts Explorer")
    topic_ids = [t["id"] for t in topic_data]
    selected = st.sidebar.selectbox("Select Topic", topic_ids, key="posts_topic")
    topic = next(t for t in topic_data if t["id"] == selected)

    st.subheader(f"Topic {topic['id']} — Top Words")
    top_n_default = 10
    top_n_expanded = 20
    # Show top 10 as pills
    pills_html = "".join(f"<span class='pill'>{w}</span>" for w in topic["words"][:top_n_default])
    st.markdown(pills_html, unsafe_allow_html=True)
    # Expander for words 11-20
    with st.expander("Show words 11–20"):
        pills_expanded = "".join(
            f"<span class='pill'>{w}</span>" 
            for w in topic["words"][top_n_default:top_n_expanded]
        )
        st.markdown(pills_expanded, unsafe_allow_html=True)

    st.subheader("Sampled 10 Posts")
    # Highlight top-10 in posts
    for post in topic["posts"][0:10]:
        highlighted = highlight_text(post, topic["words"][:top_n_default])
        st.markdown(f"- {highlighted}", unsafe_allow_html=True)

    with st.expander("Show posts 11-20"):
        for post in topic["posts"][10:20]:
            highlighted = highlight_text(post, topic["words"][:top_n_expanded])
            st.markdown(f"- {highlighted}", unsafe_allow_html=True)

# --- Comments Explorer ---
else:
    st.title("💬 Comments Explorer")
    comment_ids = [c["id"] for c in comments_data]
    selected = st.sidebar.selectbox("Select Topic", comment_ids, key="comments_topic")
    comment_group = next(c for c in comments_data if c["id"] == selected)

    st.subheader(f"Topic {comment_group['id']} — Top Words")
    top_n_default = 10
    top_n_expanded = 20
    top50_count = 50

    pills_html = "".join(f"<span class='pill'>{w}</span>" for w in comment_group["words"][:top_n_default])
    st.markdown(pills_html, unsafe_allow_html=True)

    with st.expander("Show top 20 words"):
        pills_expanded = "".join(f"<span class='pill'>{w}</span>" for w in comment_group["words"][:top_n_expanded])
        st.markdown(pills_expanded, unsafe_allow_html=True)

    with st.expander("Show top 50 words"):
        pills_top50 = "".join(f"<span class='pill'>{w}</span>" for w in comment_group["words"][:top50_count])
        st.markdown(pills_top50, unsafe_allow_html=True)

    st.subheader(f"Topic {comment_group['id']} — Sampled 10 Comments")
    for comment in comment_group.get('posts', [])[:10]:
        highlighted = highlight_text(comment, comment_group["words"][:top_n_default])
        st.markdown(f"- {highlighted}", unsafe_allow_html=True)

    with st.expander("Show comments 11-20"):
        for comment in comment_group.get('posts', [])[10:20]:
            highlighted = highlight_text(comment, comment_group["words"][:top_n_default])
            st.markdown(f"- {highlighted}", unsafe_allow_html=True)

    with st.expander("Show comments 21-30"):
        for comment in comment_group.get('posts', [])[20:30]:
            highlighted = highlight_text(comment, comment_group["words"][:top_n_default])
            st.markdown(f"- {highlighted}", unsafe_allow_html=True)
