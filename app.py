
import streamlit as st
from groq import Groq
import re

# =========================================
# PAGE CONFIG
# =========================================
st.set_page_config(
    page_title="AI: The Master Story Teller",
    page_icon="⚡",
    layout="wide"
)

# =========================================
# API CONFIG
# =========================================
client = Groq(api_key="gsk_XXXX")

# =========================================
# SESSION STATES
# =========================================
if "generated_story" not in st.session_state:
    st.session_state.generated_story = ""

# =========================================
# THEME COLORS (Fixed to Dark Theme)
# =========================================
bg_overlay = "transparent"  
card_bg = "rgba(20,20,20,0.7)" 
text_color = "#ffffff"
input_bg = "#1f1f1f"

# =========================================
# CUSTOM CSS
# =========================================
def apply_custom_styles():
    st.markdown(f"""
    <style>

    /* Remove Streamlit's default top padding and empty space */
    .block-container {{
        padding-top: 2rem !important;
        padding-bottom: 1rem !important;
        max-width: 1200px;
    }}
    
    /* Hide the default Streamlit header (hamburger menu & deploy button) */
    header {{
        visibility: hidden;
    }}

    /* Entire App - Using the Storytelling image as background */
    .stApp {{
        background-image: url("https://alvarotrigo.com/blog/assets/imgs/2021-12-24/what-is-storytelling-website-design.jpeg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: {text_color};
    }}

    /* Main Overlay */
    .main-overlay {{
        background: {bg_overlay};
        padding: 10px 30px; /* Reduced top padding */
        border-radius: 25px;
    }}

    /* Hero Banner */
    .hero-banner {{
        background: linear-gradient(
            135deg,
            rgba(108,99,255,0.9),
            rgba(0,212,255,0.8)
        );
        padding: 30px; /* Slightly tighter padding */
        border-radius: 25px;
        text-align: center;
        margin-bottom: 25px;
        backdrop-filter: blur(12px);
        box-shadow: 0px 10px 30px rgba(0,0,0,0.4);
    }}

    .hero-banner h1 {{
        font-size: 3.5rem; /* Slightly scaled down so everything fits */
        margin-bottom: 5px;
        background: linear-gradient(90deg, #ffffff, #dcdcff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    
    .hero-banner p {{
        font-size: 1.1rem;
        color: white;
        margin-bottom: 0px;
    }}
    
    /* Input Box Label (Transparent Oval Box) */
    .stTextInput label p {{
        color: #000000 !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        background-color: rgba(255, 255, 255, 0.4) !important;
        border-radius: 25px !important;
        padding: 5px 15px !important;
        display: inline-block !important;
        border: 1px solid rgba(0, 0, 0, 0.2) !important;
        margin-bottom: 5px !important;
    }}

    /* Input Box */
    .stTextInput > div > div > input {{
        background-color: {input_bg} !important;
        color: {text_color} !important;
        border-radius: 15px !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        padding: 14px !important;
    }}
    
    /* Center the Form Submit Button */
    [data-testid="stFormSubmitButton"] {{
        display: flex;
        justify-content: center;
        margin-top: 15px;
    }}

    [data-testid="stFormSubmitButton"] button {{
        width: 300px !important;
        background: linear-gradient(90deg, #6c63ff, #00d4ff);
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 15px !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        transition: 0.3s ease;
    }}
    
    /* Processing/Spinner Text (Transparent Oval Box) */
    div.stSpinner > div > div > p, [data-testid="stSpinner"] p {{
        color: #000000 !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        background-color: rgba(255, 255, 255, 0.4) !important;
        border-radius: 25px !important;
        padding: 5px 15px !important;
        display: inline-block !important;
        border: 1px solid rgba(0, 0, 0, 0.2) !important;
    }}

    /* Story Container */
    .story-container {{
        background: {card_bg};
        backdrop-filter: blur(8px); /* Reduced blur so background is much clearer */
        padding: 35px;
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.15); 
        margin-top: 20px;
        color: {text_color};
        max-height: 450px; 
        overflow-y: auto;
        box-shadow: 0px 5px 20px rgba(150,150,150,0.3);
    }}

    /* Remove Sidebar Divider/Partition lines */
    section[data-testid="stSidebar"] hr {{
        display: none;
    }}

    section[data-testid="stSidebar"] {{
        background: rgba(0,0,0,0.4);
        backdrop-filter: blur(10px);
    }}

    </style>
    """, unsafe_allow_html=True)

# =========================================
# AI FUNCTION (Updated to force Title and Story format)
# =========================================
def get_ai_story(user_prompt):
    try:
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system", 
                    "content": """You are a creative, friendly children's book author. Write fun, engaging, and simple short stories for kids. 
                    You MUST format your EXACT response using these tags:
                    <TITLE>The Title Goes Here</TITLE>
                    <STORY>The story text goes here...</STORY>
                    Do not use asterisks, hashtags, or any other markdown."""
                },
                {"role": "user", "content": f"Write a compelling short story for kids about: {user_prompt}"}
            ],
            model="llama-3.3-70b-versatile"
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# =========================================
# MAIN APP
# =========================================
def main():
    apply_custom_styles()
    
    # =========================
    # MAIN CONTAINER
    # =========================
    st.markdown('<div class="main-overlay">', unsafe_allow_html=True)

    # HERO SECTION
    st.markdown(
    """
    <div class="hero-banner">
        <h1>⚡ SwiftScribe AI</h1>
        <p>Create cinematic AI-generated stories instantly</p>
    </div>
    """,
    unsafe_allow_html=True
    )

    # FORM
    with st.form("story_form"):
        user_input = st.text_input(
            "📖 Enter your story idea:",
            placeholder="Enter your Prompt here..."
        )
        submitted = st.form_submit_button("Generate Masterpiece")

    # GENERATE & DISPLAY
    if submitted:
        if user_input.strip():
            with st.spinner("Crafting your Story..."):
                st.session_state.generated_story = get_ai_story(user_input)
        else:
            st.warning("⚠️ Please enter a story idea!")

    if st.session_state.generated_story:
        raw_text = st.session_state.generated_story
        
        # 1. Safely extract using our strict XML tags
        title_match = re.search(r'<TITLE>(.*?)</TITLE>', raw_text, re.DOTALL | re.IGNORECASE)
        story_match = re.search(r'<STORY>(.*?)</STORY>', raw_text, re.DOTALL | re.IGNORECASE)
        
        if title_match and story_match:
            story_title = title_match.group(1).strip()
            story_body = story_match.group(1).strip()
        else:
            story_title = "A Magical Tale"
            # Cleanup if the AI forgot the tags
            story_body = raw_text.replace('<TITLE>', '').replace('</TITLE>', '').replace('<STORY>', '').replace('</STORY>', '').strip()
            
        # 2. Aggressively strip any accidental asterisks or hashes
        story_title = story_title.replace('*', '').replace('#', '').strip()
        story_body = story_body.replace('*', '')

        # 3. Use INLINE CSS to force the center and underline, bypassing Streamlit class overrides
        st.markdown(f"""
        <div class="story-container">
            <div style="text-align: center; font-weight: bold; text-decoration: underline; font-size: 2rem; margin-bottom: 25px; color: #ffffff; width: 100%;">
                {story_title}
            </div>
            <div style="line-height: 1.9; font-size: 1.1rem; white-space: pre-wrap; color: #ffffff;">
                {story_body}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()