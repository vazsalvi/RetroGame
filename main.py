import openai

# Your OpenAI API key
api_key = "YOUR_API_KEY"

# Initialize OpenAI API
openai.api_key = api_key

# Function to interact with GPT
def chat_with_gpt(user_input):
    try:
        # Send a request to the OpenAI API (using the new chat endpoint)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use gpt-3.5-turbo or gpt-4
            messages=[{"role": "user", "content": user_input}],
        )
        # Extract the response text from the API response
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"

# Chatbot loop
print("ChatGPT Chatbot (Type 'exit' to quit)")
while True:
    user_input = input("You: ").strip()
    if user_input.lower() == "exit":
        print("Chatbot: Goodbye! Have a nice day!")
        break
    # Send user input to the ChatGPT model and get the response
    response = chat_with_gpt(user_input)
    print(f"Chatbot: {response}")
