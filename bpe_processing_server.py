import os
from argparse import ArgumentParser

from flask import Flask, jsonify
from flask import make_response
from flask import request
from flask import render_template

from bpe_tokenizer.bpe_state import BpeState
from bpe_tokenizer.util import load_from_file

#app = Flask(__name__, static_url_path='')
app = Flask(__name__)
state = BpeState()


@app.route('/process', methods=['POST'])
def handle_input_text():
    body = request.get_json()
    text_to_process = body['text']

    response = {
        'status': 'ok',
        'processed_text': ''.join([state.encode(word) for word in text_to_process.split()])
    }

    return make_response(jsonify(response), 200)

@app.route('/')
def root():
    return render_template("index.html")

if '__main__' == __name__:
    parser = ArgumentParser()

    parser.add_argument('-t', '--table-path', help='Path to BPE table', required=True)
    parser.add_argument('-p', '--port', help='Server port', default=5000, type=int)

    args = parser.parse_args()

    if not os.path.exists(args.table_path):
        print('Specified table does not exist ({path})'.format(path=args.table_path))
        exit(1)

    state = load_from_file(args.table_path)
    app.run(port=args.port)
