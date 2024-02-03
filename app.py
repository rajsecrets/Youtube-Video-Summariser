import streamlit as st
from dotenv import load_dotenv

load_dotenv()
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


from youtube_transcript_api import YouTubeTranscriptApi


# getting the transcript data from youtube videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id =youtube_video_url.split("=")[1]
        print(video_id)
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)

        transcript =""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript
    except Exception as e:
        raise e


# getting the summary from google gemini

prompt = """
you are a youtube video summariser , you take the transcript text and 
summaries the entire video and providing the important summary inpoints within 250 words
the transcript text will be appended here 
give the results in points and sub points :
"""

def generate_gemini_content(transcript_text,prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt+transcript_text)
    return response.text


st.title("Youtube Video Summariser")
youtube_link = st.text_input("Enter YouTube Video Link")

if youtube_link:
    video_id=youtube_link.split("=")[1]
    print(video_id)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
if st.button("Get Notes"):
    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        summary=generate_gemini_content(transcript_text, prompt)
        st.markdown("## Notes")
        st.write(summary)