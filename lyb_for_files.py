def read_keywords_and_cities(file_name):
    """
    Reads a file and returns a list of words.

    Args:
        file_name (str): The path to the file.

    Returns:
        list: A list of words extracted from the file.

    """
    
    with open(file_name, 'r') as f:
        data = f.read()
        word_list = [word.strip() for word in data.split(',')]
    return word_list

#print(readFile('keywords.txt'))