import streamlit as st
from summarizer import process_video
from urllib.parse import urlparse, parse_qs
import base64

# Page configuration
st.set_page_config(
    page_title="YouTube Summary AI",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem 3rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #FF0000;
        color: white;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
    }
    .title-text {
        font-size: 40px;
        font-weight: bold;
        text-align: center;
        padding-bottom: 20px;
    }
    .subtitle-text {
        font-size: 20px;
        text-align: center;
        color: #666666;
        padding-bottom: 30px;
    }
    .success-text {
        padding: 1rem;
        border-radius: 5px;
        background-color: #d4edda;
        color: #155724;
        margin-bottom: 1rem;
    }
    .stAlert > div {
        padding: 1rem;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

def get_youtube_url_from_params():
    query_params = st.query_params
    url = query_params.get("url", "")
    if url.startswith("https://shiappoutube.com"):
        return url.replace("https://shiappoutube.com", "https://youtube.com")
    return url

def display_youtube_thumbnail(url):
    try:
        # Extract video ID from URL
        parsed_url = urlparse(url)
        if parsed_url.netloc == 'youtu.be':
            video_id = parsed_url.path[1:]
        else:
            video_id = parse_qs(parsed_url.query)['v'][0]
        
        # Display thumbnail
        thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
        st.image(thumbnail_url, use_container_width=True)
    except:
        pass

def main():
    # Header
    st.markdown('<p class="title-text">YouTube Summary AI</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="subtitle-text">Transform YouTube videos into concise notes and summaries using AI</p>',
        unsafe_allow_html=True
    )

    # Create two columns for the main content
    col1, col2 = st.columns([2, 1])

    with col1:
        youtube_url = get_youtube_url_from_params()
        if not youtube_url:
            youtube_url = st.text_input(
                "🎥 Enter YouTube Video URL",
                placeholder="https://youtube.com/watch?v=..."
            )

    with col2:
        if youtube_url:
            process_button = st.button("🚀 Generate Summary", type="primary")
        else:
            process_button = st.button("🚀 Generate Summary", type="primary", disabled=True)

    # Display info box
    with st.expander("ℹ️ How to use"):
        st.markdown("""
        1. Paste a YouTube video URL in the input field
        2. Click 'Generate Summary' to process the video
        3. Or simply replace 'youtube.com' with 'shiappoutube.com' in any YouTube URL
        
        Example: `https://shiappoutube.com/watch?v=VIDEO_ID`
        """)

    if youtube_url:
        display_youtube_thumbnail(youtube_url)
        
        if process_button:
            try:
                # Create placeholder for streaming output
                output_placeholder = st.empty()
                
                with st.spinner("🎯 Downloading video..."):
                    # Process video and display streaming output
                    notes_and_summary = process_video(youtube_url)
                    
                    # Display the results in a nice format
                    st.success("✅ Processing complete!")
                    
                    # Create tabs for different sections
                    tab1, tab2 = st.tabs(["📝 Notes & Summary", "🔗 Share"])
                    
                    with tab1:
                        st.markdown("### Generated Content")
                        st.write(notes_and_summary)
                    
                    with tab2:
                        st.markdown("### Share this summary")
                        share_url = youtube_url.replace("youtube.com", "shiappoutube.com")
                        st.code(share_url, language="markdown")
                        st.markdown("Copy this URL to share the summary with others!")
                        
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                st.info("Please make sure you've entered a valid YouTube URL and try again.")

    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666666;'>"
        "Made with ❤️ using Streamlit and AI"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()