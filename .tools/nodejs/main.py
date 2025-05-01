import asyncio
from autogen_agentchat.agents import AssistantAgent
from together import Together
import os
import requests
import re


TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
url = "https://api.together.xyz/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {TOGETHER_API_KEY}",
    "Content-Type": "application/json",
}
SYSTEM_PROMPT = """ONLY USE HTML, CSS AND JAVASCRIPT. If you want to use ICON make sure to import the library first. Try to create the best UI possible by using only HTML, CSS and JAVASCRIPT. Use as much as you can TailwindCSS for the CSS, if you can't do something with TailwindCSS, then use custom CSS (make sure to import <script src="https://cdn.tailwindcss.com"></script> in the head). Also, try to ellaborate as much as you can, to create something unique. ALWAYS GIVE THE RESPONSE INTO A SINGLE HTML FILE.
"""
# AI_MODEL = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"
# AI_MODEL="Qwen/Qwen3-235B-A22B-fp8-tput"
AI_MODEL = "deepseek-ai/DeepSeek-V3"
data = {
    "model": AI_MODEL,
    "messages": [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": "Design an ecommerce web like amazon.com",
        },
    ],
    "temperature": 0.8,
    "top_p": 0.9,
    "max_tokens": 130000,
}


async def main() -> None:
    response = requests.post(url, headers=headers, json=data)
    print(response.json())
    html_content = (
        response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
    )
    match = re.search(
        r"<!DOCTYPE html>.*?</html>", html_content, re.DOTALL | re.IGNORECASE
    )
    if match:
        html_content = match.group(0)
    else:
        html_content = ""
    print(html_content)
    if html_content:
        with open("./index.html", "w", encoding="utf-8") as f:
            f.write(html_content)


asyncio.run(main())
