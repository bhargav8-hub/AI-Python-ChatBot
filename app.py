from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv
import random
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = Flask(__name__)

# Configuration
DEEPINFRA_URL = "https://api.deepinfra.com/v1/openai/chat/completions"
MODEL_NAME = "meta-llama/Llama-2-70b-chat-hf"
API_KEY = os.getenv('DEEPINFRA_API_KEY', '')

# Python demo responses
DEMO_RESPONSES = {
    'greetings': [
        "Hello! I'm in Python mode, ready to assist!",
        "Hi there! This is Python mode, nice to meet you!",
        "Hey! Python mode activated, what's up?",
        "Greetings! I'm your Python-powered assistant.",
        "Hello! Python mode here, how can I help?",
        "Hi! I'm running in local Python mode.",
        "Hey there! Python mode is on, let's chat!",
        "Hello! I'm your friendly Python chatbot.",
        "Hi! Python mode engaged, what's next?",
        "Greetings! Ready to answer in Python style!"
    ],
    'name_response': [
        "Nice to meet you, {name}! I'm your Python assistant.",
        "Hey {name}, great name! How can I assist you today?",
        "{name}, that's cool! I'm in Python mode, ready to help.",
        "Hi {name}! Python mode here, what's your question?",
        "Wow, {name}, nice to know! What's up in Python mode?",
        "Hello {name}! I'm your Python-powered chatbot, let's talk!",
        "Hey {name}, Python mode is on. What's on your mind?",
        "{name}, awesome to meet you! Ready to answer in Python!",
        "Hi {name}! I'm here in Python mode, what's next?",
        "{name}, great to meet you! What's up?"
    ],
    'how_are_you': [
        "I'm doing great in Python mode, thanks for asking!",
        "I'm just a bunch of code, but I'm feeling awesome!",
        "Python mode is running smoothly, how about you?",
        "I'm a happy Python chatbot, thanks for asking!",
        "All good in Python land, what's good with you?",
        "I'm thriving in Python mode, how are you?",
        "Chilling in Python mode, feeling great!",
        "I'm a script, but I'm doing fantastic, thanks!",
        "Python mode is treating me well, how about you?",
        "I'm as good as a clean Python script, thanks!"
    ],
    'how_work': [
        "I work by running Python code locally with predefined responses!",
        "In Python mode, I pick from a set of coded replies to chat.",
        "I'm a Python script selecting responses based on your input!",
        "I process your message and reply from my Python database.",
        "Python mode uses local logic to generate my answers.",
        "I match your words to my Python response bank to reply!",
        "I'm a simple Python chatbot using coded responses.",
        "In Python mode, I rely on pre-written replies, no AI!",
        "I scan your message and choose a Python-crafted response.",
        "I work by selecting from my Python response list!"
    ],
    'thanks': [
        "You're welcome! Python mode appreciates that!",
        "No problem, happy to help in Python mode!",
        "Thanks for the thanks! Python mode rocks!",
        "You're very welcome, Python style!",
        "Glad I could help in Python mode!",
        "Thanks! Python mode is here for you!",
        "You're welcome, courtesy of Python mode!",
        "No worries, Python mode's got you!",
        "Thanks for that! Python mode keeps it simple!",
        "Happy to assist in Python mode!"
    ],
    'what_is_python': [
        "Python is a versatile programming language known for its simplicity!",
        "Python is a high-level language for web, data science, and more.",
        "It's an easy-to-learn language used in many fields!",
        "Python is a powerful tool for coding apps and automation.",
        "Think of Python as a friendly language for all kinds of programs!",
        "Python makes coding fun with its clear, readable syntax!",
        "It's an open-source language for tons of cool projects.",
        "Python is a general-purpose language, great for all skill levels!",
        "Python powers websites, AI, and data analysis with ease.",
        "It's a flexible language loved for its ease of use!"
    ],
    'how_python_works': [
        "Python interprets code line by line, making debugging easy!",
        "It runs your code through an interpreter to machine instructions.",
        "Python executes scripts with an interpreter, no compilation needed!",
        "Your Python code is run by an interpreter in real-time.",
        "It translates your code into actions a computer understands.",
        "Python's interpreter processes code, great for quick testing!",
        "It runs your Python script directly, line by line.",
        "Python uses an interpreter to execute code on the fly.",
        "It processes code via an interpreter, no pre-compiling needed!",
        "Python runs code through an interpreter for fast development!"
    ],
    'what_is_ai': [
        "AI is tech that mimics human intelligence, like learning and solving problems!",
        "Artificial Intelligence lets computers think like humans for tasks.",
        "AI gives machines the ability to think and learn a bit like us!",
        "It's tech that helps computers reason and make decisions.",
        "AI stands for Artificial Intelligence, enabling smart systems.",
        "AI creates systems that learn from data and act intelligently.",
        "It's tech that lets machines do complex tasks like humans!",
        "Artificial Intelligence is software that learns and adapts.",
        "AI uses data to make smart choices or predictions.",
        "It's like teaching machines to think and solve problems!"
    ],
    'explain_ai': [
        "AI is about machines learning from data to perform smart tasks!",
        "Artificial Intelligence mimics human thinking, like reasoning or learning.",
        "AI involves algorithms that let computers adapt and decide.",
        "It's tech that processes data to mimic human intelligence.",
        "AI systems learn patterns to solve problems or predict outcomes.",
        "Think of AI as computers getting smarter with experience!",
        "AI uses models to understand and respond to complex inputs.",
        "It's like giving machines a brain to learn and act!",
        "AI processes data to make decisions, like humans do.",
        "Artificial Intelligence is tech that evolves with data!"
    ],
    'questions': [
        "Great question! In Python mode, I keep it simple.",
        "Hmm, let me think... Here's a Python mode reply!",
        "Good one! I'm answering from my Python responses.",
        "Interesting question! Python mode has a simple answer.",
        "Let me check my Python replies... Here you go!",
        "Nice question! I'm digging into my Python answers.",
        "Python mode here, here's a quick answer!",
        "Cool question for Python mode to handle!",
        "Let me pull a Python response for you!",
        "In Python mode, I have a basic reply for you."
    ],
    'default': [
        "I'm using local Python responses, what's next?",
        "Python mode here, keeping it simple!",
        "This is a Python-powered reply, ask away!",
        "In Python mode, I give basic responses like this.",
        "Just a simple Python reply for you!",
        "Python mode activated, what's your next question?",
        "Here's a Python-crafted response for you!",
        "In Python mode, I keep things straightforward.",
        "Python mode reply: Let's keep chatting!",
        "This is Python mode, what's on your mind?"
    ],
    'error': [
        "Oops, Python mode can't handle that one!",
        "Sorry, that's a bit tricky for Python mode.",
        "Python mode here, try a different question!",
        "I didn't catch that in Python mode, try again?",
        "Python mode error: Let's try something else.",
        "That one's tough for Python mode, another question?",
        "Python mode can't process that, what's next?",
        "Sorry, Python mode needs a clearer question!",
        "Python mode says: Let's try another one!",
        "Hmm, Python mode is stumped, try again?"
    ]
}

def get_demo_response(user_message):
    logger.info(f"Processing Python mode message: {user_message}")
    user_message = user_message.lower()
    
    # Check for name introduction (e.g., "my name is bhargav")
    if 'my name is' in user_message:
        name = user_message.split('my name is')[-1].strip().split()[0].capitalize()
        return random.choice(DEMO_RESPONSES['name_response']).format(name=name)
    
    # Prioritize AI and Python-related questions
    if 'what is ai' in user_message or 'what\'s ai' in user_message:
        return random.choice(DEMO_RESPONSES['what_is_ai'])
    elif any(term in user_message for term in ['explain ai', 'about ai', 'tell me about ai', 'describe ai']):
        return random.choice(DEMO_RESPONSES['explain_ai'])
    elif 'what is python' in user_message or 'what\'s python' in user_message:
        return random.choice(DEMO_RESPONSES['what_is_python'])
    elif 'how' in user_message and 'python' in user_message and any(term in user_message for term in ['work', 'function', 'run', 'operate']):
        return random.choice(DEMO_RESPONSES['how_python_works'])
    
    # Other specific patterns
    if any(greet in user_message for greet in ['hi', 'hello', 'hey']):
        return random.choice(DEMO_RESPONSES['greetings'])
    elif 'how are you' in user_message or 'how you doing' in user_message:
        return random.choice(DEMO_RESPONSES['how_are_you'])
    elif 'how' in user_message and any(term in user_message for term in ['work', 'function', 'operate']) and not any(term in user_message for term in ['python', 'ai', 'artificial']):
        return random.choice(DEMO_RESPONSES['how_work'])
    elif any(word in user_message for word in ['thank', 'thanks']):
        return random.choice(DEMO_RESPONSES['thanks'])
    elif '?' in user_message:
        return random.choice(DEMO_RESPONSES['questions'])
    else:
        return random.choice(DEMO_RESPONSES['default'])

def get_ai_response(user_message):
    logger.info(f"Processing AI mode message: {user_message}")
    if not API_KEY:
        logger.error("No API key provided for AI mode")
        return "AI Error: No API key configured"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": user_message}],
        "temperature": 0.7,
        "max_tokens": 150
    }

    try:
        response = requests.post(
            DEEPINFRA_URL,
            headers=headers,
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        logger.error(f"AI API error: Status {response.status_code}")
        return f"AI Error: Status {response.status_code}"
    except Exception as e:
        logger.error(f"AI API exception: {str(e)}")
        return f"AI Error: {str(e)}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = data.get('message', '')
    mode = data.get('mode', 'AI').lower()  # Get mode from frontend, case-insensitive
    
    if not user_message.strip():
        logger.warning("Empty message received")
        return jsonify({'response': "Please enter a valid message"}), 400
    
    if mode == 'python':
        logger.info("Handling request in Python mode")
        bot_response = get_demo_response(user_message)
    else:
        logger.info("Handling request in AI mode")
        bot_response = get_ai_response(user_message)
    
    return jsonify({
        'response': bot_response,
        'mode': mode
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)