import flask
import sys
import time 
import shutil
import code_engine
import bridge_utils
import os
from flask import request, jsonify
from io import StringIO
from contextlib import redirect_stdout
from flask_cors import CORS, cross_origin
from bridge_utils import code_to_file
from flask import stream_with_context, request


app = flask.Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/init', methods=['POST'])
@cross_origin()
def init():
  body = request.get_json()
  userid = str(body['id'])
  file_path = f"tmp/{userid}"

  if userid:
    if not os.path.exists(file_path):
      os.mkdir(file_path)
      f = open(f"{file_path}/main.py", "w")
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

@app.route('/files/getlist', methods=['POST']) # Ok
@cross_origin()
def get_list_from_index():
    body = request.get_json()
    userid = str(body['id'])
    file_path = f"tmp/{userid}" 
    testarr = []
    
    if os.path.exists(file_path):
        for root, directories, files in os.walk(file_path, topdown=False):
            for name in files:
                testarr.append(os.path.join(root, name))
            for name in directories:
                testarr.append(os.path.join(root, name))


    print({'output': testarr})
    
    return {'output': testarr}
    # await time.sleep(20)
    
    return str(testarr)

@app.route('/files/getcontent', methods=['POST']) # Ok
@cross_origin()
def get_content():
  body = request.get_json()
  userid = str(body['id'])
  posted_path = str(body['path'])
  file_path = f"tmp/{userid}/{posted_path}"

  if userid and posted_path:
			if os.path.exists(file_path):
				output = open(file_path, "r").read()
			else:
				output = "[ERR] Could Not Open File."
  else:
    output = "[ERR] Missing Body Values."

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

  return {
    'needs_input': needs_input,
    'output': output
  }
  # await time.sleep(20)
  
  return str(output)

@app.route('/folder/deletefolder', methods=['POST']) # Ok
@cross_origin()
def delete_folder():
	body = request.get_json()
	userid = str(body['id'])
	posted_path = str(body['path'])
	file_path = f"tmp/{userid}/{posted_path}"

	try:
		shutil.rmtree(file_path)
		output = f"Sucessfully Deleted: {posted_path}"
	except FileNotFoundError:
		output = '[ERR] Couldn\'t delete the specified folder'

	return output


@app.route('/folder/createfolder', methods=['POST']) # OK
@cross_origin()
def create_folder():
	body = request.get_json()
	userid = str(body['id'])
	posted_path = str(body['path'])
	file_path = f"tmp/{userid}/{posted_path}"

	try:
		os.mkdir(file_path)
		output = f"Sucessfully Created: {posted_path}"
	except FileNotFoundError:
		output = '[ERR] Couldn\'t create the specified folder.'
	
	return output


@app.route('/folder/renamefolder', methods=['POST']) # OK
@cross_origin()
def rename_folder():
    body = request.get_json()
    userid = str(body['id'])
    posted_path = str(body['path'])
    new_name = str(body['name'])
    file_path = f"tmp/{userid}/{posted_path}"
    new_path = f"tmp/{userid}/{new_name}"

    try:
        os.rename(file_path, new_path)
        output = f"Sucessfully Renamed: {posted_path}"
    except FileNotFoundError:
        output = '[ERR] Couldn\'t rename the specified folder.'
    
    return output

# ===============================

@app.route('/files/deletefile', methods=['POST'])
@cross_origin()
def delete_file():
    body = request.get_json()
    userid = str(body['id'])
    posted_path = str(body['path'])
    file_path = f"tmp/{userid}/{posted_path}"

    try:
        os.remove(file_path)
        output = f"Sucessfully Deleted: {posted_path}"
    except FileNotFoundError:
        output = '[ERR] Couldn\'t delete the specified file.'

    return output


@app.route('/files/createfile', methods=['POST']) # Ok
@cross_origin()
def create_file():
    body = request.get_json()
    userid = str(body['id'])
    posted_path = str(body['path'])
    file_path = f"tmp/{userid}/{posted_path}"

    try:
        f = open(file_path, 'x')
        f.close()
        output = f"Sucessfully Created: {posted_path}"
    except FileNotFoundError:
        output = '[ERR] Couldn\'t create the specified file.'
    
    return output


@app.route('/files/renamefile', methods=['POST']) # Ok
@cross_origin()
def rename_file():
    body = request.get_json()
    userid = str(body['id'])
    posted_path = str(body['path'])
    new_name = str(body['name'])
    file_path = f"tmp/{userid}/{posted_path}"
    new_path = f"tmp/{userid}/{new_name}"

    try:
        os.rename(file_path, new_path)
        output = f"Sucessfully Renamed: {posted_path}"
    except FileNotFoundError:
        output = '[ERR] Couldn\'t rename the specified file.'
    
    return output


@app.route('/files/write', methods=['POST']) # Ok
@cross_origin()
def write_file():
    body = request.get_json()
    userid = str(body['id'])
    posted_path = str(body['path'])
    content = str(body['content'])
    file_path = f"tmp/{userid}/{posted_path}"

    try:
        file = open(file_path, "w")
        file.write(content)
        file.close()
        output = f"Sucessfully Updated: {posted_path}"
    except FileNotFoundError:
        output = '[ERR] Couldn\'t write to the specified file.'
    
    return output

@app.route('/')
@cross_origin()
def fun():
  return '<b>Pussy HEe Hee</b>'

app.run(host="0.0.0.0", port=8000)