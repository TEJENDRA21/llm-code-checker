import os
from openai import OpenAI
from flask import Flask, render_template_string

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

@app.route('/')
def display_result():
    # Example code to check
    code = """
    def example_function():
        # TODO: Implement this function
        pass
    """
    result = check_code_with_llm(code)
    # Render the result in a simple HTML template
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>LLM Code Analysis</title>
    </head>
    <body>
        <h1>LLM Code Check Result</h1>
        <pre>{{ result }}</pre>
    </body>
    </html>
    """
    return render_template_string(html_template, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
