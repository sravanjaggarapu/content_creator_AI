from openai import OpenAI
from flask import Flask, request, render_template_string
import os
from dotenv import load_dotenv

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Content Generator</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f9f9f9; text-align: center; padding: 50px; }
        form { margin: 20px auto; width: 50%; }
        textarea { width: 100%; height: 100px; padding: 10px; font-size: 16px; }
button {
            margin-top: 15px;
            background-color: #2563eb;
            color: #ffffff;
            border: none;
            padding: 12px 24px;
            border-radius: 6px;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        button:hover {
            background-color: #1e40af;
        }        
        .output { margin-top: 30px; background-color: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
    </style>
</head>
<body>
    <h1>AI Content Generator</h1>
    <form method="POST">
        <textarea name="input" placeholder="Enter a topic for your Content..."></textarea><br>
        <button type="submit">Generate Content</button>
    </form>
    {% if poem %}
    <div class="output">
        <h2>Your AI-Generated Poem:</h2>
        <p>{{ poem.replace('\\n', '<br>')|safe }}</p>
    </div>
    {% endif %}
</body>
</html>
"""

load_dotenv()

app = Flask(__name__)

client = OpenAI(
    api_key= os.environ.get("OPENAI_API"),
    base_url= os.environ.get("LLM_ENDPOINT")
)

@app.route("/", methods=["GET","POST"])
def index():
    poem = None
    if request.method == "POST":
        try:
            input_message = request.form["input"]

            model_name = os.getenv("MODEL_OLLAMA", "llama3")  # fallback to llama3


            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "You are a content creating AI"},
                    {"role": "user", "content": input_message}
                ]
            )
            poem = response.choices[0].message.content
            
        except Exception as e:
            print("Error: ", str(e))
            poem = "An error occured while we are trying solve your request"

    return render_template_string(HTML_TEMPLATE, poem=poem)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 3000))
    app.run(host="0.0.0.0", port=port)