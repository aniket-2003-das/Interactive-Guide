import openai


# Fetch the initial input from the backend
initial_input = """ Give Initial Input Here"""

openai.api_key = 'Your_Api_Key'

def get_openai_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Initialize conversation history
conversation_history = ""

# Fetch the initial input from the backend
conversation_history += initial_input

# Continue with user input from the terminal
while True:
    user_input = input("You: ")  # Take user input from the terminal
    if user_input.lower() == 'exit':
        break

    # Add user input to the conversation history
    conversation_history += "\nYou: " + user_input

    # Get response from OpenAI based on the entire conversation history
    openai_response = get_openai_response(conversation_history)

    # Add OpenAI's response to the conversation history
    conversation_history += "\nChatbot: " + openai_response

    print("Chatbot:", openai_response)

