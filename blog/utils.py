from gtts import gTTS
import html2text
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification

def generate_audio(blog_content, audio_file_path):
    plain_text = html2text.html2text(blog_content)

    tts = gTTS(text=plain_text, lang='en')
    tts.save(audio_file_path)

def send_push_notification(title,body,data=None):
    data = data or {}
    message = Message(
        notification=Notification(title=title, body=body, image="url"),
        data=data,
    )
    
    devices = FCMDevice.objects.all()
    devices.send_message(message)