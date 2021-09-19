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

"""
Create, Remove, Read, Write, Rename File
Create, Remove, Rename Folder

"""

app = flask.Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/init', methods=['POST'])
@cross_origin()
def init():
  body = request.get_json()
  userid = str(body['id'])
  user_path = f"tmp/{userid}"

  if userid:
    if not os.path.exists(user_path):
      os.mkdir(user_path)
      f = open(f"{user_path}/main.py", "w")
      f.write("""print("Hello World!")""")
      f.close()
      output = "[200] Successfully Initialized A User."
    else:
      output = "[200] The User Has Already Been Initialized. Skipping..."
  else:
    output = "[ERR] Missing ID Param."


  print({
    'output': output
    
  })

  return {
    'output': output
  }
  # await time.sleep(20)
  
  return str(output)

@app.route('/files/getlist', methods=['GET']) # List of the files in the directory
@cross_origin()
def get_list_from_index():
    body = request.get_json()
    userid = str(body['id'])
    user_path = f"tmp/{userid}" 
    testarr = []
    
    if os.path.exists(user_path):
        for root, directories, files in os.walk(user_path, topdown=False):
            for name in files:
                testarr.append(os.path.join(root, name))
            for name in directories:
                testarr.append(os.path.join(root, name))


    print({'output': testarr})
    
    return {'output': testarr}
    # await time.sleep(20)
    
    return str(testarr)

@app.route('/files/getcontent', methods=['POST'])
@cross_origin()
def getcontent():
  body = request.get_json()
  userid = str(body['id'])
  file_path = 

  if userid:
    if not os.path.exists(user_path):
      os.mkdir(user_path)
      f = open(f"{user_path}/main.py", "w")
      f.write("""print("Hello World!")""")
      f.close()
      output = "[200] Successfully Initialized A User."
    else:
      output = "[200] The User Has Already Been Initialized. Skipping..."
  else:
    output = "[ERR] Missing ID Param."

  print({
    'output': output
  })

  return {
    'output': output
  }
  # await time.sleep(20)
  
  return str(output)

@app.route('/run', methods=['POST'])
@cross_origin()
def run():
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


@app.route('/folder/delete', methods=['GET'])
@cross_origin()
def delete_folder():
    body = request.get_json()
    userid = str(body['id'])
    user_path = f"tmp/{userid}"

    try:
        os.rmdir(user_path)
    except FileNotFoundError:
        print('Couldn\'t find specified folder')

    return None


@app.route('/folder/create', methods=['GET'])
@cross_origin()
def create_folder():
    body = request.get_json()
    userid = str(body['id'])
    user_path = f"tmp/{userid}"

    try:
        os.mkdir(user_path)
    except FileNotFoundError:
        print('Couldn\'t find specified folder')

    return None


@app.route('/folder/rename', methods=['GET'])
@cross_origin()
def rename_folder():
    body = request.get_json()
    userid = str(body['id'])
    user_path = f"tmp/{userid}"

    try:
        os.rename(user_path)
    except FileNotFoundError:
        print('Couldn\'t specified folder')

    return None