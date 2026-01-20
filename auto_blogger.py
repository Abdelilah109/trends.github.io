import os
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from openai import OpenAI

# --- 1. CONFIGURATION ---
OR_KEY = os.environ.get("OPENROUTER_API_KEY")

# 2026 Strict Auth Handshake
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=OR_KEY,
  default_headers={
    "HTTP-Referer": "https://github.com/karroumiabdo580", # REQUIRED: Use your real GitHub URL
    "X-Title": "Blogger AutoBot 2026",                 # REQUIRED: Any name works
    "User-Agent": "Mozilla/5.0 (Script)"                # Helps bypass "Cookie" checks
  }
)

def generate_content(keyword):
    print(f"🤖 Requesting content for: {keyword}")
    try:
        completion = client.chat.completions.create(
          model="google/gemini-2.0-flash-lite-preview:free",
          messages=[
            {"role": "user", "content": f"Write a professional 1200-word blog post about '{keyword}' in clean HTML. Use H2 headers."}
          ],
          extra_headers={
              "HTTP-Referer": "https://github.com/karroumiabdo580",
          }
        )
        return completion.choices[0].message.content
    except Exception as e:
        # Catching the exact 401 and explaining why
        if "401" in str(e):
            print("❌ AUTH ERROR: OpenRouter rejected the key. Check if your key has credits or if it's the 'sk-or-v1' type.")
        raise e

# ... (keep the rest of your publish_post() code)
