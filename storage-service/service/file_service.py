import os 

def create_file(file_name, text):
    with open(file_name + '.txt', 'w') as file:
        file.write(text)

    return file_name + '.txt' 

def remove_file(file_name):
    os.remove(file_name)