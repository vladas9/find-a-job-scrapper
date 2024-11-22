def read_file(file_name):
    with open(file_name, 'r') as f:
        data = f.read()
        word_list = [word.strip() for word in data.split(',')]
    return word_list

#print(readFile('keywords.txt'))