import openai

# Set your OpenAI API key here
openai.api_key = 'Your_Api_Key'

def generate_title_recap(url):
    # Define the prompt for the OpenAI GPT-3 model
    prompt = f"Generate a title and a quick recap in points under it about the webpage at {url}"

    # Use the OpenAI GPT-3 API to generate the title recap
    response = openai.Completion.create(
        engine="text-davinci-002",  # You can experiment with other engines
        prompt=prompt,
        max_tokens=500  # You can adjust this based on the desired length
    )

    # Extract and return the generated title recap
    title_recap = response['choices'][0]['text']
    return title_recap

# Example usage:
url_to_process = "https://en.wikipedia.org/wiki/Atom"
result = generate_title_recap(url_to_process)
print(f"Title Recap for {url_to_process}:\n{result}")
