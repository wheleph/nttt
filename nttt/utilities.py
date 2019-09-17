from shutil import copy2, copystat, Error, ignore_patterns
import os
import os.path
import codecs

def get_file(file_name):
    with codecs.open(file_name, encoding='utf-8') as f:
        return f.read()

def save_file(file_name, s):
    with codecs.open(file_name, encoding='utf-8', mode="w") as f:
        f.write(s)

def find_snippet(s, start_string, end_string):
    start_pos = s.find(start_string)
    if start_pos > -1:
        start_of_snippet = start_pos + len(start_string)
        end_pos = s.find(end_string, start_of_snippet)
        return s[start_of_snippet:end_pos]
    else:
        return None

def find_replace(src, dst, find, replace):
    with codecs.open(src, encoding='utf-8') as f:
        s = f.read()
    s = s.replace(find, replace)
    with codecs.open(dst, encoding='utf-8', mode="w") as f:
        f.write(s)

def find_files(src, file_names=[], extensions=[]):
    files_found = []

    for dname, dirs, files in os.walk(src):
        for fname in files:
            fpath = os.path.join(dname, fname)          
            
            # check file_names and extensions
            valid_file = False
            
            if len(extensions) > 0:
                ext = os.path.splitext(fpath)
                if ext[-1] in extensions:
                    valid_file = True

            if len(file_names) > 0:
                if fname in file_names:
                    valid_file = True
            
            # if we arent checking file_names or extension it must be valid
            if len(extensions) == 0 and len(file_names) == 0:
                valid_file = True

            if valid_file:
                files_found.append(fpath)

    return files_found