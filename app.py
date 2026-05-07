import streamlit as st
from groq import Groq

# --- CONFIGURATION ---
# Replace with your actual key
client = Groq(api_key="GROQ_API_KEY")

# --- 1. SESSION STATE INITIALIZATION ---
# This ensures the story doesn't disappear when the app reruns
if "generated_story" not in st.session_state:
    st.session_state.generated_story = ""

# --- 2. CSS STYLING ---
def apply_custom_styles():
    st.markdown("""
        <style>
        .stApp { background: #0e1117; color: #e0e0e0; }
        h1 { color: #6c63ff; text-align: center; font-family: 'Segoe UI', sans-serif; }
        
        /* Input Box */
        .stTextInput > div > div > input {
            background-color: #1a1c24 !important;
            color: white !important;
            border: 1px solid #3e4149 !important;
            border-radius: 10px !important;
        }

        /* Fixed Button Logic */
        div.stButton > button {
            width: 100%;
            background: linear-gradient(90deg, #6c63ff 0%, #3f37c9 100%);
            color: white !important;
            border-radius: 12px !important;
            border: none !important;
            padding: 15px !important;
            font-weight: bold !important;
            font-size: 1.1rem !important;
            transition: 0.3s;
        }
        
        div.stButton > button:hover {
            transform: scale(1.02);
            box-shadow: 0px 5px 15px rgba(108, 99, 255, 0.4);
        }

        .story-container {
            background-color: #1a1c24;
            padding: 25px;
            border-radius: 15px;
            border-left: 6px solid #6c63ff;
            margin-top: 25px;
            line-height: 1.8;
            white-space: pre-wrap; /* Preserves paragraphs */
        }
        </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIC FUNCTION ---
def get_ai_story(user_prompt):
    try:
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a master storyteller."},
                {"role": "user", "content": f"Write a compelling short story about: {user_prompt}"}
            ],
            model="llama-3.3-70b-versatile",
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# --- 4. MAIN APP ---
def main():
    apply_custom_styles()
    
    st.markdown("<h1>⚡ SwiftScribe AI</h1>", unsafe_allow_html=True)
    
    # Input field
    user_input = st.text_input("Enter your idea:", placeholder="A lost city under the Arabian Sea...")

    # Button logic
    if st.button("Generate Masterpiece"):
        if user_input.strip():
            with st.spinner("Writing..."):
                # Store the result in session state
                st.session_state.generated_story = get_ai_story(user_input)
        else:
            st.warning("Please type something first!")

    # Display the story if it exists in session state
    if st.session_state.generated_story:
        st.markdown(f"""
            <div class="story-container">
                {st.session_state.generated_story}
            </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()