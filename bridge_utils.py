import os
import time


def code_to_file(code, language, id):
    print("Processing the code into a file.")
    file_path = "tmp/" + str(id) + language_extension(language)
    file = open(file_path, "w")
    file.write(code)
    file.close()
    return file_path


def input_file(code, language, id):
    print("Processing the input into a file.")
    input_path = "tmp/" + str(id) + ".input"
    file = open(input_path, "w")
    file.write(code)
    file.close()
    return input_path


def cleanup(file_path, input_path):
    if os.path.exists(file_path):
        os.remove(file_path)
    if os.path.exists(input_path):
        os.remove(input_path)


def language_extension(language):
    extensions = {"python": ".py"}
    return extensions[language]


def generate_files(code, language, id):
  code_path = code_to_file(code, language, id)
  input_path = input_file(code, language, id)
  return code_path, input_path


# if __name__ == "__main__":
#     path = code_to_file("""print("Hello")""", "python", 123456)
#     time.sleep(3)
#     cleanup(path)
