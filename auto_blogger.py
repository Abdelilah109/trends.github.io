import os
import smtplib
import random
import time
import requests
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- CONFIGURATION ---
OR_KEY = os.environ.get("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")
BLOGGER_EMAIL = "karroumiabdo580.aipost@blogger.com"
SENDER_EMAIL = "karroumiabdo580@gmail.com" 
SENDER_PASSWORD = "arojzxofkobgtpdk" 

# Using the most stable 2026 free model via OpenRouter
MODEL_NAME = "google/gemini-2.0-flash-lite-preview:free"

topics = [
    "How to Scale a Faceless AI YouTube Channel in 2026",
    "Is 2026 the Year AI Agents Replace Entry-Level Jobs?",
    "The Best Free AI Tools for Digital Marketing (2026 Edition)",
    "How to build a sustainable passive income with AI Blogging"
]
target_keyword = random.choice(topics)

def generate_content(keyword):
    print(f"🤖 Requesting blog post from OpenRouter: {keyword}...")
    
    headers = {
        "Authorization": f"Bearer {OR_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/karroumiabdo580", # Required by OpenRouter
    }
    
    data = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user", 
                "content": f"Write a high-quality, 1500-word blog post about '{keyword}'. Use clean HTML with H2 headers, bold text, and bullet points. Make it viral and professional."
            }
        ]
    }
    
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        data=json.dumps(data)
    )
    
    result = response.json()
    
    if 'choices' in result:
        return result['choices'][0]['message']['content']
    else:
        raise Exception(f"AI Error: {result}")

def publish_post():
    try:
        print(f"🚀 Starting process for: {target_keyword}")
        content = generate_content(target_keyword)
        
        # Image via Pollinations AI (Free)
        img_url = f"https://image.pollinations.ai/prompt/tech_blog_{target_keyword.replace(' ','_')}?width=1080&height=720&nologo=true"
        
        html_body = f"""
        <div style="font-family: Arial, sans-serif; line-height: 1.8; color: #333;">
            <img src="{img_url}" style="width:100%; border-radius:15px; margin-bottom: 25px;">
            <div style="font-size: 16px;">
                {content}
            </div>
            <hr style="margin: 40px 0; border-top: 1px solid #eee;">
            <p style="text-align: center; color: #888;"><i>Post generated automatically by AI FastTrack #end.</i></p>
        </div>
        """

        msg = MIMEMultipart()
        msg['Subject'] = target_keyword
        msg['From'] = SENDER_EMAIL
        msg['To'] = BLOGGER_EMAIL
        msg.attach(MIMEText(html_body, 'html'))
        
        print("📧 Logging into Gmail and sending to Blogger...")
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, BLOGGER_EMAIL, msg.as_string())
        server.quit()
        
        print(f"✅ SUCCESS! Your post '{target_keyword}' is now on your blog.")
        
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {str(e)}")

if __name__ == "__main__":
    publish_post()
