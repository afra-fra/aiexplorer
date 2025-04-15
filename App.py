import streamlit as st
import json

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

# Custom CSS for security text loaded afterwards
st.markdown(
    """
    <style>
      .security-text {
         font-size: 28 px !important;
      }
    </style>
    """,
    unsafe_allow_html=True
)


# Define your security question and answer
security_question = "What’s the key to success?"
security_answer = "luck"  # answer is stored in lowercase

# Initialize authentication state if not already set
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown('<p class="security-text">Please answer the security question to access this web:</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="security-text"><strong>{security_question}</strong></p>', unsafe_allow_html=True)
    user_answer = st.text_input("Your Answer:")
    if user_answer:
        if user_answer.strip().lower() == security_answer:
            st.session_state.authenticated = True
        else:
            st.error("Incorrect answer. Please try again.")
# Only stop if still not authenticated
if not st.session_state.authenticated:
    st.stop()  # stops execution until the correct answer is given


# Optional: bump up font size


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

    st.subheader(f"Topic {topic['id']} — Top Words")
    # Filter out stop words (comparison in lowercase).
    top_n_default = 10
    top_n_expanded = 20
    top50_count = 50
    # Display the top 10 words as styled "pill" elements.
    pills_html = "".join(f"<span class='pill'>{w}</span>" for w in topic["words"][:top_n_default])
    st.markdown(pills_html, unsafe_allow_html=True)
    # Use an expander to reveal more words (e.g. top 20).
    with st.expander("Show top 20 words"):
        pills_expanded = "".join(f"<span class='pill'>{w}</span>" for w in topic["words"][:top_n_expanded])
        st.markdown(pills_expanded, unsafe_allow_html=True)
    # Expander for top 50 words
    with st.expander("Show top 50 words"):
      pills_top50 = "".join(f"<span class='pill'>{w}</span>" for w in topic["words"][:top50_count])
      st.markdown(pills_top50, unsafe_allow_html=True)

    st.subheader("Sampled 10 Posts")
    for post in topic["posts"]:
        st.markdown(f"- {post}")

else:  # Comments Explorer
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
    for comment in comment_group.get("posts", []):
        st.markdown(f"- {comment}")

