import os
from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")  # Fetch API key from environment variable
)

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

def main():
    # Example code to check
    code = """
    def example_function():
        # TODO: Implement this function
        pass
    """
    result = check_code_with_llm(code)
    print(f"LLM Check Result:\n{result}")

if __name__ == "__main__":
    main()
