import os
from flask import Flask, request, render_template_string
from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")  # Fetch API key from environment variable
)

app = Flask(__name__)

def check_code_with_llm(code):
    """Check the code using an LLM."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI assistant that reviews Python code for issues, best practices, and suggestions.",
                },
                {
                    "role": "user",
                    "content": f"Check the following Python code for issues:\n\n{code}",
                },
            ],
        )
        # Access the message content correctly
        message_content = response.choices[0].message.content
        return message_content.strip()
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    if request.method == 'POST':
        code = request.form.get('code')
        if code:
            result = check_code_with_llm(code)

    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>LLM Code Checker</title>
    </head>
    <body>
        <h1>LLM Code Checker</h1>
        <form method="POST">
            <textarea name="code" rows="10" cols="80" placeholder="Paste your Python code here"></textarea><br>
            <button type="submit">Check Code</button>
        </form>
        {% if result %}
            <h2>LLM Check Result:</h2>
            <pre>{{ result }}</pre>
        {% endif %}
    </body>
    </html>
    """
    return render_template_string(html_template, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
