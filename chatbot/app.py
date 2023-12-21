# Import necessary libraries
from flask import Flask, render_template, request

import spacy

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# Define a dictionary where keys are questions and values are answers
qa_pairs = {
    "你叫什么名字？": "我是ChatGPT，您的聊天机器人。",
    "你会做什么？": "我可以回答一些基本问题。",
    "如何学习编程？": "学习编程需要不断练习，阅读文档，参加课程，解决问题，不断学习。"
}

# Initialize Flask application
app = Flask(__name__)

# Define a route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Define a route for handling user queries
@app.route('/ask', methods=['POST'])
def ask():
    # Get user input from the form
    user_input = request.form['user_input']

    # Use spaCy to process user input
    doc = nlp(user_input)

    # Initialize response
    response = "我不明白您的问题。"

    # Look for a matching question in the QA pairs
    for question, answer in qa_pairs.items():
        if doc.similarity(nlp(question)) > 0.7:  # Set similarity threshold
            response = answer
            break

    return render_template('index.html', user_input=user_input, response=response)

if __name__ == '__main__':
    app.run(debug=True)

