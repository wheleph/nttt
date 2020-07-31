from shutil import copy2, copystat, Error, ignore_patterns
import os
import os.path
import codecs
import re

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


#PUB-9 utilities. These methods are for trimming spaces on specific markdown like ** or _. The main method is trim_spaces_on_specific_markdown which uses trim_spaces_on_specific_markdown_breakdown and strings_with_specific_markdown_and_spaces.
 

regular_expressions_matrix_for_trimming_spaces = [
    {'character':'_', 'regular_expression_for_wrong_left':r"_[ ]+[a-z]+[ ]*_", 'regular_expression_for_wrong_right':r"_[ ]*[a-z]+[ ]+_", "regular_expression_for_correct":r"_[a-z]*_"},
    {'character':'`', 'regular_expression_for_wrong_left':r"`[ ]+[a-z]+[ ]*`", 'regular_expression_for_wrong_right':r"`[ ]*[a-z]+[ ]+`", "regular_expression_for_correct":r"`[a-z]*`"},
    {'character':'<asterisk>', 'regular_expression_for_wrong_left':r"<asterisk>[ ]+[a-z]+[ ]*<asterisk>", 'regular_expression_for_wrong_right':r"<asterisk>[ ]*[a-z]+[ ]+<asterisk>", "regular_expression_for_correct":r"<asterisk>[a-z]*<asterisk>"},
    {'character':'*', 'regular_expression_for_wrong_left':r"\*[ ]+[a-z]+[ ]*\*", 'regular_expression_for_wrong_right':r"\*[ ]*[a-z]+[ ]+\*", "regular_expression_for_correct":r"\*[a-z]*\*"},
    ]

corrections_for_trimming_spaces = [
    {'character':'_', 'left_space':"_ ", 'right_space':" _"},
    {'character':'`', 'left_space':"` ", 'right_space':" `"},
    {'character':'<asterisk>', 'left_space':"<asterisk> ", 'right_space':" <asterisk>"},
    {'character':'*', 'left_space':"* ", 'right_space':" *"},
    ]

def trim_spaces_on_specific_markdown(content):
    content = content.replace("**", "<asterisk>")
    for i in [0, 1, 2, 3]:
        character_on_focus = regular_expressions_matrix_for_trimming_spaces[i]['character']
        problematic_strings_left = re.findall(regular_expressions_matrix_for_trimming_spaces[i]['regular_expression_for_wrong_left'], content)
        problematic_strings_right = re.findall(regular_expressions_matrix_for_trimming_spaces[i]['regular_expression_for_wrong_right'], content)
        problematic_strings = list(set(problematic_strings_left) | set(problematic_strings_right))

        # while problematic_strings != []:
        #     problematic_string = problematic_strings[0]
        #     modified_string = problematic_string
        #     while True:
        #         modified_string = modified_string.replace(corrections_for_trimming_spaces[i]['left_space'], character_on_focus)
        #         modified_string = modified_string.replace(corrections_for_trimming_spaces[i]['right_space'], character_on_focus)        
        #         if bool(re.search(regular_expressions_matrix_for_trimming_spaces[i]['regular_expression_for_correct'], modified_string)):
        #             break
        #     content = content.replace(problematic_string, modified_string)
        #     problematic_strings = re.findall(regular_expressions_matrix_for_trimming_spaces[i]['regular_expression_for_wrong'], content)
            
        for problematic_string in problematic_strings:
            modified_string = problematic_string
            while True:
                modified_string = modified_string.replace(corrections_for_trimming_spaces[i]['right_space'], character_on_focus)        
                modified_string = modified_string.replace(corrections_for_trimming_spaces[i]['left_space'], character_on_focus)
                if bool(re.search(regular_expressions_matrix_for_trimming_spaces[i]['regular_expression_for_correct'], modified_string)):
                    break
            content = content.replace(problematic_string, modified_string)
#            problematic_strings = re.findall(regular_expressions_matrix_for_trimming_spaces[i]['regular_expression_for_wrong'], content)

    content = content.replace("<asterisk>", "**")
    return content        