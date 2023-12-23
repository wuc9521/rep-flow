import os
import spacy
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, request, jsonify
from flask_cors import cross_origin
import pandas as pd


# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

df = pd.read_csv('./data/qa.csv')
qa = dict(zip(df['Q'], df['A']))

# Initialize Flask application
app = Flask(__name__)

# Configure logging
log_dir = os.path.join(app.root_path, 'log')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file_path = os.path.join(log_dir, f"flask.log")

formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] [%(module)s] - %(message)s")
handler = RotatingFileHandler(log_file_path, maxBytes=10000, backupCount=1)
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)


@app.route('/')
def home():
    app.logger.info("Home page request")
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
@cross_origin(supports_credentials=True)
def ask():
    try:
        data = request.get_json()
        query_text = data['query']
        
        response = "Sorry, I don't understand what you are asking."
        doc = nlp(query_text)
        for question, answer in qa.items():
            if doc.similarity(nlp(question)) > 0.7:  # Set similarity threshold
                response = answer
                break
        if response == "Sorry, I don't understand what you are asking.":
            app.logger.info(f"User query: {query_text} - No answer found")
        return jsonify({"answer": response})
    except Exception as e:
        app.logger.error(f"{str(e)}")
        return jsonify({"error": "An error occurred"}), 500


if __name__ == '__main__':
    app.run(debug=True)