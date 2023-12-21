# Import necessary libraries
from flask import Flask, render_template, request
import pandas as pd
import spacy

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

df = pd.read_csv('./data/qa.csv')
print(df.columns)
qa = dict(zip(df['Q'], df['A']))

# Initialize Flask application
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.form['user_input']
    # Use spaCy to process user input
    doc = nlp(user_input)

    # Initialize response
    response = "Sorry, I don't understand what you are asking."

    # Look for a matching question in the QA pairs
    for question, answer in qa.items():
        if doc.similarity(nlp(question)) > 0.7:  # Set similarity threshold
            response = answer
            break

    return render_template('index.html', user_input=user_input, response=response)

if __name__ == '__main__':
    app.run(debug=True)
