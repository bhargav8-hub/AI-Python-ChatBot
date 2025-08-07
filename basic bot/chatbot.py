import random

# Response dictionary
DEMO_RESPONSES = {
    'greetings': [
        "Hello! I'm in Python mode, ready to assist!",
        "Hi there! This is Python mode, nice to meet you!",
        "Hey! Python mode activated, what's up?",
        "Greetings! I'm your Python-powered assistant.",
        "Hello! Python mode here, how can I help?"
    ],
    'name_response': [
        "Nice to meet you, {name}! I'm your Python assistant.",
        "Hey {name}, great name! How can I assist you today?",
        "Hi {name}! Python mode here, what's your question?"
    ],
    'how_are_you': [
        "I'm doing great in Python mode, thanks for asking!",
        "I'm just a bunch of code, but I'm feeling awesome!",
        "Python mode is running smoothly, how about you?"
    ],
    'how_work': [
        "I work by running Python code locally with predefined responses!",
        "I'm a Python script selecting responses based on your input!"
    ],
    'thanks': [
        "You're welcome! Python mode appreciates that!",
        "No problem, happy to help in Python mode!"
    ],
    'what_is_python': [
        "Python is a versatile programming language known for its simplicity!",
        "Python is a high-level language for web, data science, and more."
    ],
    'how_python_works': [
        "Python interprets code line by line, making debugging easy!",
        "Python executes scripts with an interpreter, no compilation needed!"
    ],
    'what_is_ai': [
        "AI is tech that mimics human intelligence, like learning and solving problems!",
        "Artificial Intelligence lets computers think like humans for tasks."
    ],
    'explain_ai': [
        "AI is about machines learning from data to perform smart tasks!",
        "Artificial Intelligence mimics human thinking, like reasoning or learning."
    ],
    'questions': [
        "Great question! In Python mode, I keep it simple.",
        "Nice question! I'm digging into my Python answers."
    ],
    'default': [
        "I'm using local Python responses, what's next?",
        "This is a Python-powered reply, ask away!"
    ],
    'error': [
        "Oops, Python mode can't handle that one!",
        "Sorry, that's a bit tricky for Python mode."
    ]
}

def get_response(user_message):
    user_message = user_message.lower().strip()

    # Name detection
    if 'my name is' in user_message:
        name = user_message.split('my name is')[-1].strip().split()[0].capitalize()
        return random.choice(DEMO_RESPONSES['name_response']).format(name=name)

    if any(greet in user_message for greet in ['hi', 'hello', 'hey']):
        return random.choice(DEMO_RESPONSES['greetings'])
    if 'how are you' in user_message or 'how you doing' in user_message:
        return random.choice(DEMO_RESPONSES['how_are_you'])
    if 'thank' in user_message:
        return random.choice(DEMO_RESPONSES['thanks'])
    if 'what is python' in user_message or "what's python" in user_message:
        return random.choice(DEMO_RESPONSES['what_is_python'])
    if 'how python' in user_message and any(word in user_message for word in ['work', 'run', 'function']):
        return random.choice(DEMO_RESPONSES['how_python_works'])
    if 'what is ai' in user_message or "what's ai" in user_message:
        return random.choice(DEMO_RESPONSES['what_is_ai'])
    if any(phrase in user_message for phrase in ['explain ai', 'about ai', 'describe ai']):
        return random.choice(DEMO_RESPONSES['explain_ai'])
    if 'how' in user_message and any(w in user_message for w in ['work', 'function', 'operate']):
        return random.choice(DEMO_RESPONSES['how_work'])
    if '?' in user_message:
        return random.choice(DEMO_RESPONSES['questions'])

    return random.choice(DEMO_RESPONSES['default'])

# Run chatbot loop
def chat():
    print("ChatBot (Python Mode): Hello! Type 'bye' to exit.")
    while True:
        user_message = input("You: ")
        if user_message.strip().lower() in ['bye', 'exit', 'quit']:
            print("ChatBot: Bye! Have a great day!")
            break
        print("ChatBot:", get_response(user_message))

# Start
if __name__ == "__main__":
    chat()
