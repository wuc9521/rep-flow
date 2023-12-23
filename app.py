import os
import spacy
import logging
import pandas as pd
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import cross_origin
# from .model.hist import test_hist

DEFAULT_RESPONSE_FLAG = "*"


# Load spaCy English model
nlp = spacy.load("en_core_web_sm")
app = Flask(__name__)

# Configure
LOG_DIR = os.path.join(app.root_path, 'log')
DATA_DIR = os.path.join(app.root_path, 'data')
MODEL_DIR = os.path.join(app.root_path, 'model')
CSV_DIR = os.path.join(DATA_DIR, 'csv')

std = pd.read_csv(os.path.join(CSV_DIR, 'std.csv'))
df = pd.merge(
    pd.read_csv(os.path.join(CSV_DIR, 'qa.csv')),
    std,
    on='ID',
    how='left'
)
qa = dict(zip(
    df['Q'],
    df['A']
))
at = dict(zip(
    std['A'],
    std['TYPE']
))

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
log_file_path = os.path.join(LOG_DIR, f"app.log")

formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] [%(module)s] - %(message)s")
handler = RotatingFileHandler(log_file_path, maxBytes=10000, backupCount=1)
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)
app.logger.info(f"QA pairs: {qa}")


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/images/<filename>')
def serve_image(filename):
    # 使用 send_from_directory 提供图片服务
    return send_from_directory(os.path.join(DATA_DIR, 'state'), filename)


@app.route('/ask', methods=['POST'])
@cross_origin(supports_credentials=True)
def ask():
    try:
        data = request.get_json()
        query_text = data['query']

        response = qa.get(DEFAULT_RESPONSE_FLAG)
        doc = nlp(query_text)
        for question, answer in qa.items():
            if doc.similarity(nlp(question)) > 0.7:  # Set similarity threshold
                response = answer
                break
        if response == qa.get(DEFAULT_RESPONSE_FLAG):
            app.logger.warning(
                f"User query: \"{query_text}\" - No answer found")
            return jsonify({
                "type": at.get(DEFAULT_RESPONSE_FLAG),
                "answer": qa.get(DEFAULT_RESPONSE_FLAG)
            }), 200
        app.logger.info(f"User query: \"{query_text}\" - Answer: {response}")
        app.logger.info("Current State: {}".format(get_current_state()))
        return jsonify({
            "type": at.get(response),
            "answer": response,
            "img": str(get_current_state()) if get_current_state() != "Loading" else None
        }), 200
    except Exception as e:
        app.logger.error(f"{str(e)}")
        return jsonify({"error": "An error occurred"}), 500


def get_current_state():
    IMG_DIR = os.path.join(DATA_DIR, 'state')
    imgs = [f for f in os.listdir(
        IMG_DIR) if os.path.isfile(os.path.join(IMG_DIR, f))]
    if not imgs or len(imgs) == 0:
        return "Loading"  # 如果目录为空，返回None或适当的默认值
    max_file = max(
        imgs,
        key=lambda f: os.path.getctime(os.path.join(IMG_DIR, f))
    )
    if max_file.startswith("."):
        return "Loading"
    return max_file


if __name__ == '__main__':
    app.run(debug=True)
