from flask import Flask, render_template, request, session
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = "bst$chatbot_!secret@12345"

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("models/gemini-1.5-flash")

@app.route("/", methods=["GET", "POST"])
def index():
    if "chat_history" not in session:
        session["chat_history"] = []

    if request.method == "POST":
        user_input = request.form["user_input"]

        try:
            result = model.generate_content(user_input)
            ai_response = result.text
        except Exception as e:
            ai_response = f"Error: {e}"

        # Add both user and AI messages to session chat history
        session["chat_history"].append({"role": "user", "text": user_input})
        session["chat_history"].append({"role": "ai", "text": ai_response})
        session.modified = True

    return render_template("index.html", chat_history=session["chat_history"])

if __name__ == "__main__":
    app.run(debug=True)
