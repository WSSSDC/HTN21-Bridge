import flask
import sys
import time 
from flask import request, jsonify
from io import StringIO
from contextlib import redirect_stdout
from flask_cors import CORS, cross_origin
from bridge_utils import code_to_file
from flask import stream_with_context, request
import code_engine
import bridge_utils
import os


app = flask.Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/run', methods=['POST'])
@cross_origin()
def index():
  body = request.get_json()
  code = body['code']
  language = body['language']
  thread_id = str(body['id'])
  input_arr = body['input']
  # code_to_file(code, language, id)
  output_path, input_path = bridge_utils.generate_files(code, language, thread_id)
  needs_input, output = code_engine.run(thread_id, output_path, input_arr, language, code)

  print({
    'needs_input': needs_input,
    'output': output
  })

  return {
    'needs_input': needs_input,
    'output': output
  }
  # await time.sleep(20)
  
  return str(output)

app.run(host="0.0.0.0", port=8000)