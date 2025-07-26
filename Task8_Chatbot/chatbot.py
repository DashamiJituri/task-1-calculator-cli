print("🤖 Hello! I'm ChatBot. Type 'bye' to exit.")

while True:
    user_input = input("You: ").lower()

    if user_input in ["hi", "hello"]:
        print("Bot: Hello! How can I help you?")
    elif user_input in ["how are you", "how are you?"]:
        print("Bot: I'm just code, but I'm doing great!")
    elif user_input in ["bye", "exit", "quit"]:
        print("Bot: Goodbye! Have a great day!")
        break
    elif "name" in user_input:
        print("Bot: I am a simple chatbot created using Python.")
    else:
        print("Bot: Sorry, I didn't understand that.")
