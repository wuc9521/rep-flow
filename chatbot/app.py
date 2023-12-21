# Import necessary libraries
from flask import Flask, render_template, request, jsonify
from flask_cors import cross_origin
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
        return jsonify({"answer": response})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "An error occurred"}), 500

if __name__ == '__main__':
    app.run(debug=True)
