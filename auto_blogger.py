import os
import smtplib
import random
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google import genai
from groq import Groq

# --- CONFIGURATION ---
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
GROQ_KEY = os.environ.get("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")
BLOGGER_EMAIL = "karroumiabdo580.aipost@blogger.com"
SENDER_EMAIL = "karroumiabdo580@gmail.com" 
SENDER_PASSWORD = "arojzxofkobgtpdk" 

# 2026 Stable Models
GEMINI_MODEL = "gemini-2.0-flash-lite"
GROQ_MODEL = "llama-3.3-70b-versatile"

topics = [
    "AI Agent Workflows: Automating your life in 2026",
    "Why Groq is beating Nvidia in AI Inference speed",
    "How to use Gemini 2.0 for free business automation",
    "Top 5 AI tools that are actually free in 2026"
]
target_keyword = random.choice(topics)

def generate_with_gemini(keyword):
    client = genai.Client(api_key=GEMINI_KEY)
    prompt = f"Write a 1200 word viral blog post about {keyword} in clean HTML."
    response = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
    return response.text

def generate_with_groq(keyword):
    client = Groq(api_key=GROQ_KEY)
    prompt = f"Write a 1200 word viral blog post about {keyword} in clean HTML. Use H2 tags."
    completion = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content

def publish_post():
    print(f"🚀 Starting process for: {target_keyword}")
    time.sleep(10) # Safety delay
    
    content = ""
    try:
        print(f"🤖 Trying Gemini ({GEMINI_MODEL})...")
        content = generate_with_gemini(target_keyword)
    except Exception as e:
        if "429" in str(e) or "QUOTA" in str(e).upper():
            print("⚠️ Gemini limit reached. Switching to Groq...")
            content = generate_with_groq(target_keyword)
        else:
            print(f"❌ Gemini Error: {e}")
            return

    # Image + Wrapper
    img_url = f"https://image.pollinations.ai/prompt/cyber_tech_{target_keyword.replace(' ','_')}?width=1080&height=720"
    html_body = f'<div><img src="{img_url}" style="width:100%; border-radius:15px;"><br>{content}</div>'

    try:
        msg = MIMEMultipart()
        msg['Subject'] = target_keyword
        msg['From'] = SENDER_EMAIL
        msg['To'] = BLOGGER_EMAIL
        msg.attach(MIMEText(html_body, 'html'))
        
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, BLOGGER_EMAIL, msg.as_string())
        server.quit()
        print(f"✅ SUCCESS! Published via AI.")
    except Exception as e:
        print(f"❌ Email Error: {e}")

if __name__ == "__main__":
    publish_post()
