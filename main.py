import openai
import ffmpeg
from PIL import Image, ImageDraw, ImageFont
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# OpenAI API 
openai.api_key = os.getenv('OPENAI_API_KEY')

# YouTube API 
def youtube_authenticate():
    CLIENT_SECRETS_FILE = os.getenv('CLIENT_SECRETS_FILE')  # Load from .env file
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=["https://www.googleapis.com/auth/youtube.upload"]
    )
    credentials = flow.run_local_server(port=8081)  # Use a different port number to 8080 aldready in use by Jupyter Notebook
    youtube = build("youtube", "v3", credentials=credentials)
    return youtube

# def generate_joke_quiz():
def generate_joke_quiz():
    prompt = "one funny joke to share with friends, only answer it"
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "system", "content": "You are a funny friend."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100
    )
    quiz = response.choices[0].message['content'].strip()
    return quiz

#  def create_quiz_video(quiz_text, output_video_path):
def create_quiz_video(quiz_text, output_video_path):
    font = ImageFont.load_default()
    width, height = 800, 600
    image = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.text((20, 20), quiz_text, font=font, fill=(0, 0, 0))
    image.save('funny.png')
    ffmpeg.input('funny.png', t=15, framerate=1).output(output_video_path, vcodec='libx264').run()

# def upload_video_to_youtube(youtube, video_file, title, description):
def upload_video_to_youtube(youtube, video_file, title, description):
    try:
        request = youtube.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": title,
                    "description": description
                },
                "status": {
                    "privacyStatus": "public"
                }
            },
            media_body=video_file
        )
        response = request.execute()
        print(f"Upload successful! Video ID: {response['id']}")
    except Exception as error:
        print(f"An error occurred: {error}")

# overall flow
quiz = generate_joke_quiz()
print(f"Generated Quiz: {quiz}")

create_quiz_video(quiz, 'funny_video.mp4')

#youtube = youtube_authenticate()

#upload_video_to_youtube(youtube, 'funny_video.mp4', 'joke Quiz', 'This is an automated funny joke video created by Python.')
