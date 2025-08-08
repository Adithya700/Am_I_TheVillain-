from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
import random
import cohere

# Load environment variables from .env file
load_dotenv()

# Get your Cohere API key from environment variable
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.Client(COHERE_API_KEY)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def analyze():
    result = None
    story = ""
    if request.method == "POST":
        story = request.form.get("story", "")
        mode = request.form.get("mode", "silly")

        if mode == "silly":
            # Unhinged, encouraging villain verdicts
            verdicts = [
                "You’re not the villain, you’re the CEO of bad decisions. Keep ruining lives, boss. 💼🔥",
                "Cutting them off without explanation? Iconic. Emotional closure is for the weak. 🥂",
                "Plotting revenge? As you should. Be petty, stay pretty. 💅😈",
                "Gaslight, gatekeep, girlboss. You’ve got the trifecta down. 🧠🔑👠",
                "Forgive? Never heard of it. Hold that grudge like a family heirloom. 🕯️",
                "You didn’t overreact—you just reacted *louder*. Respect. 📢💔",
                "Absolutely villainous. But like… in a main character way. 🎮",
                "Friendship ruined, group chat destroyed, trust annihilated? You’re thriving. 🚀",
                "You’re not messy, you're the entire soap opera. Please continue. 🍿",
                "Morally wrong? Sure. But aesthetically? A masterpiece. 🎨💣"
            ]
            result = random.choice(verdicts)

        elif mode == "ai":
            # Real AI verdict using Cohere chat endpoint
            prompt = f"""
You're an expert in drama and morality. Read the story below and decide if the person is the villain or not.

Story:
\"{story}\"

Reply in a short, witty sentence giving a fun verdict like:
- “You're the villain. Full-on Disney villain energy.”
- “You might be the villain, but at least you're hot.”
- “You're innocent, but dangerously close to the edge.”

Now give your verdict:
"""
            try:
                response = co.chat(
                    model="command-r",
                    message=prompt,
                    temperature=0.8
                )
                result = response.text.strip()
            except Exception as e:
                result = f"Cohere had a meltdown: {str(e)}"

    return render_template("index.html", result=result, story=story)

if __name__ == "__main__":
    app.run(debug=True)
