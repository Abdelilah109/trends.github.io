import os
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google import genai

# --- CONFIGURATION ---
# Use the key you provided in your GitHub Secrets under GEMINI_API_KEY
GEMINI_KEY = os.environ.get("AIzaSyBUlBeSiGmx5_nGW4AyIibRGF9xveB4Fp4")
BLOGGER_EMAIL = "karroumiabdo580.aipost@blogger.com"
SENDER_EMAIL = "karroumiabdo580@gmail.com" 
SENDER_PASSWORD = "arojzxofkobgtpdk" 

client = genai.Client(api_key=GEMINI_KEY)

topics = ["Future of AI 2026", "Passive Income with AI", "Top Tech Trends"]
target_keyword = random.choice(topics)

def generate_content(keyword):
    print(f"🤖 Using Google Gemini for: {keyword}")
    # Using 2.0 Flash (latest for 2026)
    response = client.models.generate_content(
        model="gemini-2.0-flash", 
        contents=f"Write a 1200 word blog post about {keyword} in HTML."
    )
    
    img_url = f"https://image.pollinations.ai/prompt/tech_{keyword.replace(' ','_')}?width=800&height=600"
    return f'<div><img src="{img_url}"><br>{response.text}</div>'

def publish_post():
    try:
        content = generate_content(target_keyword)
        
        msg = MIMEMultipart()
        msg['Subject'] = target_keyword
        msg['From'] = SENDER_EMAIL
        msg['To'] = BLOGGER_EMAIL
        msg.attach(MIMEText(content, 'html'))
        
        print("📧 Connecting to Gmail...")
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, BLOGGER_EMAIL, msg.as_string())
        server.quit()
        print("✅ SUCCESS! Email sent to Blogger.")
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

if __name__ == "__main__":
    publish_post()
