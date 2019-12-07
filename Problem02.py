def list_from_file(filename, sep='\n'):
    """Return the content of the named file as a list of strings"""
    f = open("Prob1-masses.txt")
    file_content = f.read()
    f.close()
    return file_content.split(sep)

