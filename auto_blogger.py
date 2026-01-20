import os
import smtplib
import random
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google import genai

# --- CONFIGURATION ---
GEMINI_KEY = os.environ.get("AIzaSyBUlBeSiGmx5_nGW4AyIibRGF9xveB4Fp4")
BLOGGER_EMAIL = "karroumiabdo580.aipost@blogger.com"
SENDER_EMAIL = "karroumiabdo580@gmail.com" 
SENDER_PASSWORD = "arojzxofkobgtpdk" 

client = genai.Client(api_key=GEMINI_KEY)

topics = ["Future of AI 2026", "Best AI Tools 2026", "AI Productivity Hacks"]
target_keyword = random.choice(topics)

def generate_content(keyword):
    print(f"🤖 Asking Gemini to write about: {keyword}")
    prompt = f"Write a 1200 word blog post about {keyword} in HTML."
    response = client.models.generate_content(model="gemini-1.5-flash", contents=prompt)
    
    img_url = f"https://image.pollinations.ai/prompt/tech_{keyword.replace(' ','_')}?width=800&height=600"
    
    html_body = f'<div><img src="{img_url}"><br>{response.text}</div>'
    return html_body

def publish_post():
    try:
        content = generate_content(target_keyword)
        print("📧 Preparing email...")
        
        msg = MIMEMultipart()
        msg['Subject'] = target_keyword
        msg['From'] = SENDER_EMAIL
        msg['To'] = BLOGGER_EMAIL
        msg.attach(MIMEText(content, 'html'))
        
        print(f"🔗 Connecting to Gmail SMTP as {SENDER_EMAIL}...")
        # We use port 465 with SSL
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        
        print("📤 Sending email to Blogger...")
        server.sendmail(SENDER_EMAIL, BLOGGER_EMAIL, msg.as_string())
        
        server.quit()
        print("✅ EMAIL SENT SUCCESSFULLY - Check Sent Folder now!")
        
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {str(e)}")

if __name__ == "__main__":
    publish_post()
