import os
import spacy
import logging
import pandas as pd
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import cross_origin
from utils.loader import read_keywords_from_file
from utils.hints import HELP, get_NUMBER_EMBD_HINT, get_CURRENT_STATE_HINT, get_NEXT_STEP_HINT 
from utils.test import extract_and_validate_test_number
from utils.log import log_
from utils.file import get_i
from model.common import imgs
from model.process import image_process

DEFAULT_RESPONSE_FLAG = "*"
NUMBER_EMBD_HINT = None
CURRENT_BUG_ID = -1


# Load spaCy English model
nlp = spacy.load("en_core_web_sm")
app = Flask(__name__, template_folder='')

# Configure
LOG_DIR = os.path.join(app.root_path, 'log')
DATA_DIR = os.path.join(app.root_path, 'data')
MODEL_DIR = os.path.join(app.root_path, 'model')
CORPUS_DIR = os.path.join(DATA_DIR, 'corpus')
GUIDANCE_DIR = os.path.join(DATA_DIR, 'guidance')
STATE_DIR = os.path.join(DATA_DIR, 'state')

std = pd.read_csv(os.path.join(CORPUS_DIR, 'std.csv'))
df = pd.merge(
    pd.read_csv(os.path.join(CORPUS_DIR, 'qa.csv')),
    std,
    on='ID',
    how='left'
)
qa = dict(zip(df['Q'], df['A']))
at = dict(zip(std['A'], std['TYPE']))
ta = dict(zip(std['TYPE'], std['A']))
key_words = read_keywords_from_file(
    os.path.join(CORPUS_DIR, 'kw.txt'), app=app)


if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
log_file_path = os.path.join(LOG_DIR, f"app.log")

formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] [%(module)s] - %(message)s")
handler = RotatingFileHandler(log_file_path, maxBytes=10000, backupCount=1)
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)


@app.route('/')
def home():
    return render_template('index.html'), 200


@app.route('/states/<filename>')
def serve_image(filename):
    return send_from_directory(STATE_DIR, filename), 200

@app.route('/guidance/<filename>')
def serve_guidance(filename):
    return send_from_directory(os.path.join(GUIDANCE_DIR, CURRENT_BUG_ID), filename), 200

@app.route('/ask', methods=['POST'])
@cross_origin(supports_credentials=True)
def ask():
    try:
        data = request.get_json()
        query_text = data['query']
        rgx_num = extract_and_validate_test_number(query_text, app)
        if rgx_num is not None and rgx_num != "": # "/test $BUG"
            global NUMBER_EMBD_HINT
            NUMBER_EMBD_HINT = get_NUMBER_EMBD_HINT(rgx_num)
            global CURRENT_BUG_ID
            CURRENT_BUG_ID = rgx_num
            return jsonify({
                "type": "TEST",
                "answer": ta.get("TEST"),
                "img": None,
                "hint": NUMBER_EMBD_HINT
            }), 200
        response = qa.get(DEFAULT_RESPONSE_FLAG)
        doc = nlp(query_text)
        nouns = [token.text for token in doc if token.pos_ == "NOUN"]
        question = DEFAULT_RESPONSE_FLAG
        for question_, answer in qa.items():
            if doc.similarity(nlp(question_)) > doc.similarity(nlp(question)):
                response = answer
                question = question_
        if response == qa.get(DEFAULT_RESPONSE_FLAG) or doc.similarity(nlp(question)) < 0.7:
            app.logger.warning(
                f"User query: \"{query_text}\" - No answer found")
            if set(key_words).intersection(set(nouns)):
                return jsonify({
                    "type": "SORRY",
                    "answer": ta.get("SORRY")
                }), 200
            else:
                return jsonify({
                    "type": at.get(qa.get(DEFAULT_RESPONSE_FLAG)),
                    "answer": qa.get(DEFAULT_RESPONSE_FLAG)
                }), 200
        app.logger.info(f"User query: \"{query_text}\" - Answer: {response}")
        app.logger.info("Current State: {}".format(monitor_current_state()))
        if at.get(response) == "HELP":
            return jsonify({
                "type": at.get(response),
                "answer": response,
                "img": monitor_current_state(),
                "hint": HELP
            }), 200
        elif at.get(response) == "NEXT":
            if CURRENT_BUG_ID == -1:
                return jsonify({
                    "type": "ID-MISSING",
                    "answer": ta.get("ID-MISSING")
                }), 200
            return jsonify({
                "type": at.get(response),
                "answer": response,
                "img": get_similarist_state(CURRENT_BUG_ID),
                "hint": get_NEXT_STEP_HINT(CURRENT_BUG_ID)
            }), 200
        elif at.get(response) == "CURRENT-STATE":
            return jsonify({
                "type": at.get(response),
                "answer": response,
                "img": monitor_current_state(),
                "hint": get_CURRENT_STATE_HINT(CURRENT_BUG_ID)
            }), 200
        else:
            return jsonify({
                "type": at.get(response),
                "answer": response,
                "img": monitor_current_state(),
                "hint": None
            }), 200
    except Exception as e:
        app.logger.error(f"{str(e)}")
        return jsonify({"error": "An error occurred"}), 500


@app.teardown_appcontext
def teardown_appcontext(error=None):
    # 这个函数将在应用上下文销毁时调用
    if error is not None:
        app.logger.error(f"An error occurred: {str(error)}")


def monitor_current_state() -> str:
    IMG_DIR = os.path.join(DATA_DIR, 'state')
    imgs = [
        f for f in os.listdir(IMG_DIR) if os.path.isfile(os.path.join(IMG_DIR, f))
    ]
    if not imgs or len(imgs) == 0:
        return "Loading"  # 如果目录为空，返回None或适当的默认值
    max_file = max(
        imgs,
        key=lambda f: os.path.getctime(os.path.join(IMG_DIR, f))
    )
    if max_file.startswith("."):
        return None
    return str(max_file)


def get_similarist_state(id):
    CURRENT_BUG_DIR = os.path.join(GUIDANCE_DIR, str(id))
    IMG_CURRENT_STATE = os.path.join(DATA_DIR, 'state', monitor_current_state())
    max_file_idx, _ = image_process(
        image_user_path=IMG_CURRENT_STATE,
        image_list=imgs[int(id)-1],
        app=app
    )
    app.logger.info("max_file_idx:", max_file_idx)
    return str(get_i(CURRENT_BUG_DIR, max_file_idx))

if __name__ == '__main__':
    app.run(debug=True)