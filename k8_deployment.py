import os
from flask import Flask, request, render_template_string
import subprocess
from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")  # Fetch API key from environment variable
)

app = Flask(__name__)

def get_deployment_file_from_openai(prompt):
    """Fetch a Kubernetes deployment file dynamically using OpenAI."""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a Kubernetes expert who generates deployment files based on user prompts.",
                },
                {
                    "role": "user",
                    "content": f"Generate a Kubernetes deployment file for {prompt}.",
                },
            ],
        )
        deployment_file = response.choices[0].message.content.strip()
        return deployment_file
    except Exception as e:
        return f"An error occurred while fetching the deployment file: {e}"

def deploy_k8s_file(file_content):
    """Deploy the Kubernetes YAML file."""
    try:
        # Save the deployment file locally
        file_path = "deployment.yaml"
        with open(file_path, "w") as file:
            file.write(file_content)
        
        # Apply the file using kubectl
        result = subprocess.run(
            ["kubectl", "apply", "-f", file_path],
            capture_output=True,
            text=True,
        )
        return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return f"An error occurred while deploying the file: {e}"

@app.route('/', methods=['GET', 'POST'])
def home():
    deploy_result = None
    generated_file = None
    if request.method == 'POST':
        prompt = request.form.get('prompt')
        if prompt:
            generated_file = get_deployment_file_from_openai(prompt)
            if "Error" not in generated_file:
                deploy_result = deploy_k8s_file(generated_file)
            else:
                deploy_result = generated_file

    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Kubernetes Deployment Prompter</title>
    </head>
    <body>
        <h1>Kubernetes Deployment Prompter</h1>
        
        <h2>Generate and Deploy Kubernetes Deployment</h2>
        <form method="POST">
            <input type="text" name="prompt" placeholder="Enter prompt (e.g., nginx)">
            <button type="submit">Generate & Deploy</button>
        </form>
        {% if generated_file %}
            <h2>Generated Deployment File:</h2>
            <pre>{{ generated_file }}</pre>
        {% endif %}
        {% if deploy_result %}
            <h2>Deployment Result:</h2>
            <pre>{{ deploy_result }}</pre>
        {% endif %}
    </body>
    </html>
    """
    return render_template_string(html_template, generated_file=generated_file, deploy_result=deploy_result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
