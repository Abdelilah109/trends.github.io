import os
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google import genai

# --- 1. CONFIGURATION ---
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
# The secret email you just gave me:
BLOGGER_EMAIL = "karroumiabdo580.aipost@blogger.com"
# Your personal Gmail to SEND from:
SENDER_EMAIL = os.environ.get("SENDER_EMAIL") 
# Your Gmail App Password (16 characters):
SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD") 

client = genai.Client(api_key=GEMINI_KEY)

# --- 2. THE TOPICS (Laser Focus) ---
topics = [
    "How to build a 24/7 AI Sales Agent for $0 in 2026",
    "Gemini 1.5 Flash vs GPT-4o: Which is better for free automation?",
    "Top 10 Hidden AI tools that replaced my $500/month subscriptions",
    "The Secret Prompt that bypasses AI detectors with 99% accuracy"
]
target_keyword = random.choice(topics)

# --- 3. GENERATE HUMAN-LIKE CONTENT ---
prompt = f"""
Act as a professional tech journalist with 10 years of experience. 
Write a deep-dive, 1,500-word article about '{keyword}'.

REQUIREMENTS:
1. First-Person Perspective: Use "I tried this..." or "In my experience..." to show human 'Experience'.
2. Structure: Use H2 and H3 tags. Start with a direct answer to the main question in the first paragraph.
3. Added Value: Include a 'Secret Tip' or 'Hack' section that is not commonly found on the web.
4. Formatting: Use bullet points, bold text for key terms, and a summary table of pros/cons.
5. Search Intent: Analyze why a user would search for this and solve their specific problem.
6. FAQ: Add a 5-question FAQ at the end using FAQ schema style.

FORMAT: Output strictly in clean HTML.
"""
    response = client.models.generate_content(model="gemini-1.5-flash", contents=prompt)
    
    # 3 Images from Pollinations (Copyright Free)
    img1 = f"https://image.pollinations.ai/prompt/cinematic%20{keyword.replace(' ','%20')}%20tech?width=1080&height=720&nologo=true"
    img2 = f"https://image.pollinations.ai/prompt/detailed%20{keyword.replace(' ','%20')}%20diagram?width=800&height=500&nologo=true"
    
    html_body = f"""
    <div style="font-family: Arial, sans-serif; line-height: 1.6;">
        <img src="{img1}" style="width:100%; border-radius:12px;" alt="Header Image">
        <br>
        {response.text}
        <br>
        <img src="{img2}" style="width:100%; border-radius:12px;" alt="Technical Insight">
        <br>
        <p><i>#end.</i></p> 
    </div>
    """
    return html_body

# --- 4. SEND TO BLOGGER ---
def publish_post():
    content = generate_content(target_keyword)
    
    msg = MIMEMultipart()
    msg['Subject'] = target_keyword # This becomes the Blog Title
    msg['From'] = SENDER_EMAIL
    msg['To'] = BLOGGER_EMAIL
    msg.attach(MIMEText(content, 'html'))
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, BLOGGER_EMAIL, msg.as_string())
        print(f"✅ Success! Published: {target_keyword}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    publish_post()
