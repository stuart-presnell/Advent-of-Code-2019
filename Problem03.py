# from operator import add, mul

def list_from_file(filename, sep='\n'):
    """Return the content of the named file as a list of strings"""
    f = open(filename)
    file_content = f.read()
    f.close()
    return file_content.split(sep)

def modify_list(list, location, value):
    return list[:location] + [value] + list[(location+1):]


