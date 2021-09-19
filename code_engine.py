import subprocess
import threading
import time
from datetime import datetime
import io
from multiprocessing import Process, Queue
from io import StringIO
from contextlib import redirect_stdout
import sys


# def get_input(process):
#   while True:
#     # process.stdin.write(bytes(input("Input: \n"), 'utf-8')) # \n
#     process.communicate(bytes(bytes(input("Input: \n"), 'utf-8')))
#     time.sleep(1)


def get_out(process):
  print("GETOUTPUT")
  print(process.communicate()[0])
  while True:
    output = process.communicate()[0].decode('ascii')
    if process.poll() is not None:
      break;
    if output:
      print(output.strip())
  # rc = process.poll()
  # return rc
  

def run(thread_id, file_name, input_arr, language, code):
  ret = {'out_with_input': ''}

  def run_code(queue):
    ret = queue.get()
    contains_input = input_arr != []
    if contains_input:
      i = open('input.txt', 'w')
      i.write('\n'.join(input_arr))
      i.close()
    f = StringIO()
    with redirect_stdout(f):
      if contains_input:
        sys.stdin=open('input.txt')
      try:
        exec(code)
        queue.put(ret)
      except Exception as error:
        print(str(error))
    # await time.sleep(20)
    ret['out_with_input'] = str(f.getvalue())
    queue.put(ret)

  queue = Queue()
  queue.put(ret)

  p2 = Process(target=run_code, args=(queue,), name='Run Code')
  p2.start()
  p2.join()

  while True:
    if(p2.exitcode is not None):
      queue_data = queue.get()
      needs_input = 'EOF when reading a line' in queue_data['out_with_input']
      outdata = queue_data['out_with_input'].replace('EOF when reading a line', '')
      return needs_input, outdata