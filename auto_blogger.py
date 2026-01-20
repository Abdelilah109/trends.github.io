import os
import smtplib
import random
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from openai import OpenAI

# --- 1. CONFIGURATION ---
# Ensure your GitHub Secret is named OPENROUTER_API_KEY
OR_KEY = os.environ.get("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")
BLOGGER_EMAIL = "karroumiabdo580.aipost@blogger.com"
SENDER_EMAIL = "karroumiabdo580@gmail.com" 
SENDER_PASSWORD = "arojzxofkobgtpdk" 

# Use the official OpenRouter base URL
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=OR_KEY,
  default_headers={
    "HTTP-Referer": "https://github.com/karroumiabdo580", # Required by OpenRouter
    "X-Title": "Blogger Bot 2026", 
  }
)

topics = [
    "Top 10 Passive Income AI Tools for 2026",
    "How to Scale a Blog to 1M Users with AI Agents",
    "Why Gemini 2.0 Flash is the Future of Content",
    "2026 Guide to Automated Digital Marketing"
]
target_keyword = random.choice(topics)

def generate_content(keyword):
    print(f"🤖 Requesting content for: {keyword}")
    
    completion = client.chat.completions.create(
      model="google/gemini-2.0-flash-lite-preview:free",
      messages=[
        {
          "role": "user",
          "content": f"Write a professional 1200-word blog post about '{keyword}' in clean HTML. Use H2 headers and bold text."
        }
      ]
    )
    return completion.choices[0].message.content

def publish_post():
    try:
        print(f"🚀 Job started...")
        content = generate_content(target_keyword)
        
        # Image Generation (Free)
        img_url = f"https://image.pollinations.ai/prompt/cybertech_{target_keyword.replace(' ','_')}?width=1080&height=720&nologo=true"
        
        html_body = f"""
        <div style="font-family: sans-serif; line-height: 1.8;">
            <img src="{img_url}" style="width:100%; border-radius:15px; margin-bottom: 20px;">
            {content}
            <p style="text-align:center; color:#888;"><i>Automated via AI FastTrack 2026.</i></p>
        </div>
        """

        msg = MIMEMultipart()
        msg['Subject'] = target_keyword
        msg['From'] = SENDER_EMAIL
        msg['To'] = BLOGGER_EMAIL
        msg.attach(MIMEText(html_body, 'html'))
        
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, BLOGGER_EMAIL, msg.as_string())
        server.quit()
        
        print(f"✅ SUCCESS! Post '{target_keyword}' is live.")
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

if __name__ == "__main__":
    publish_post()
