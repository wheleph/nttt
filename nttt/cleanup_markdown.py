import os
import re

#PUB-9 utilities. These methods are for trimming spaces on specific markdown like ** or _. The main method is trim_spaces_on_specific_markdown which uses trim_spaces_on_specific_markdown_breakdown and strings_with_specific_markdown_and_spaces.
 

#please keep it for some time, it has [ ] instead of \s
# regular_expressions_matrix_for_trimming_spaces = [
#     {'character':'_', 'regular_expression_for_wrong_left':r"_[ ]+[A-Za-z0-9_]+[ ]*_", 'regular_expression_for_wrong_right':r"_[ ]*[A-Za-z0-9_]+[ ]+_", "regular_expression_for_correct":r"_[A-Za-z0-9_]*_"},
#     {'character':'`', 'regular_expression_for_wrong_left':r"`[ ]+[A-Za-z0-9_]+[ ]*`", 'regular_expression_for_wrong_right':r"`[ ]*[A-Za-z0-9_]+[ ]+`", "regular_expression_for_correct":r"`[A-Za-z0-9_]*`"},
#     {'character':'<double_asterisk>', 'regular_expression_for_wrong_left':r"<double_asterisk>[ ]+[A-Za-z0-9_]+[ ]*<double_asterisk>", 'regular_expression_for_wrong_right':r"<double_asterisk>[ ]*[A-Za-z0-9_]+[ ]+<double_asterisk>", "regular_expression_for_correct":r"<double_asterisk>[A-Za-z0-9_]*<double_asterisk>"},
#     {'character':'*', 'regular_expression_for_wrong_left':r"\*[ ]+[A-Za-z0-9_]+[ ]*\*", 'regular_expression_for_wrong_right':r"\*[ ]*[A-Za-z0-9_]+[ ]+\*", "regular_expression_for_correct":r"\*[A-Za-z0-9_]*\*"},
#     {'character':'<triple_asterisk>', 'regular_expression_for_wrong_left':r"<triple_asterisk>[ ]+[A-Za-z0-9_]+[ ]*<triple_asterisk>", 'regular_expression_for_wrong_right':r"<triple_asterisk>[ ]*[A-Za-z0-9_]+[ ]+<triple_asterisk>", "regular_expression_for_correct":r"<triple_asterisk>[A-Za-z0-9_]*<triple_asterisk>"},
#     {'character':'<double_underscore>', 'regular_expression_for_wrong_left':r"<double_underscore>[ ]+[A-Za-z0-9_]+[ ]*<double_underscore>", 'regular_expression_for_wrong_right':r"<double_underscore>[ ]*[A-Za-z0-9_]+[ ]+<double_underscore>", "regular_expression_for_correct":r"<double_underscore>[A-Za-z0-9_]*<double_underscore>"},
#     {'character':'<triple_underscore>', 'regular_expression_for_wrong_left':r"<triple_underscore>[ ]+[A-Za-z0-9_]+[ ]*<triple_underscore>", 'regular_expression_for_wrong_right':r"<triple_underscore>[ ]*[A-Za-z0-9_]+[ ]+<triple_underscore>", "regular_expression_for_correct":r"<triple_underscore>[A-Za-z0-9_]*<triple_underscore>"},
#     ]


regular_expressions_matrix_for_trimming_spaces = [
    {'character':'_', 'regular_expression_for_wrong_left':r"_\s+[A-Za-z0-9_]+\s*_", 'regular_expression_for_wrong_right':r"_\s*[A-Za-z0-9_]+\s+_", "regular_expression_for_correct":r"_[A-Za-z0-9_]*_"},
    {'character':'`', 'regular_expression_for_wrong_left':r"`\s+[A-Za-z0-9_]+\s*`", 'regular_expression_for_wrong_right':r"`\s*[A-Za-z0-9_]+\s+`", "regular_expression_for_correct":r"`[A-Za-z0-9_]*`"},
    {'character':'<double_asterisk>', 'regular_expression_for_wrong_left':r"<double_asterisk>\s+[A-Za-z0-9_]+\s*<double_asterisk>", 'regular_expression_for_wrong_right':r"<double_asterisk>\s*[A-Za-z0-9_]+\s+<double_asterisk>", "regular_expression_for_correct":r"<double_asterisk>[A-Za-z0-9_]*<double_asterisk>"},
    {'character':'*', 'regular_expression_for_wrong_left':r"\*\s+[A-Za-z0-9_]+\s*\*", 'regular_expression_for_wrong_right':r"\*\s*[A-Za-z0-9_]+\s+\*", "regular_expression_for_correct":r"\*[A-Za-z0-9_]*\*"},
    {'character':'<triple_asterisk>', 'regular_expression_for_wrong_left':r"<triple_asterisk>\s+[A-Za-z0-9_]+\s*<triple_asterisk>", 'regular_expression_for_wrong_right':r"<triple_asterisk>\s*[A-Za-z0-9_]+\s+<triple_asterisk>", "regular_expression_for_correct":r"<triple_asterisk>[A-Za-z0-9_]*<triple_asterisk>"},
    {'character':'<double_underscore>', 'regular_expression_for_wrong_left':r"<double_underscore>\s+[A-Za-z0-9_]+\s*<double_underscore>", 'regular_expression_for_wrong_right':r"<double_underscore>\s*[A-Za-z0-9_]+\s+<double_underscore>", "regular_expression_for_correct":r"<double_underscore>[A-Za-z0-9_]*<double_underscore>"},
    {'character':'<triple_underscore>', 'regular_expression_for_wrong_left':r"<triple_underscore>\s+[A-Za-z0-9_]+\s*<triple_underscore>", 'regular_expression_for_wrong_right':r"<triple_underscore>\s*[A-Za-z0-9_]+\s+<triple_underscore>", "regular_expression_for_correct":r"<triple_underscore>[A-Za-z0-9_]*<triple_underscore>"},
    ]


corrections_for_trimming_spaces = [
    {'character':'_', 'left_space':"_ ", 'right_space':" _"},
    {'character':'`', 'left_space':"` ", 'right_space':" `"},
    {'character':'<double_asterisk>', 'left_space':"<double_asterisk> ", 'right_space':" <double_asterisk>"},
    {'character':'*', 'left_space':"* ", 'right_space':" *"},
    {'character':'<triple_asterisk>', 'left_space':"<triple_asterisk> ", 'right_space':" <triple_asterisk>"},
    {'character':'<double_underscore>', 'left_space':"<double_underscore> ", 'right_space':" <double_underscore>"},
    {'character':'<triple_underscore>', 'left_space':"<triple_underscore> ", 'right_space':" <triple_underscore>"},
    ]

def mark_replacement(content):
    content = content.replace("***", "<triple_asterisk>")
    content = content.replace("**", "<double_asterisk>")
    content = content.replace("___", "<triple_underscore>")
    content = content.replace("__", "<double_underscore>")
    return content    

def mark_recovery(content):
    content = content.replace("<double_asterisk>", "**")
    content = content.replace("<triple_asterisk>", "***")
    content = content.replace("<double_underscore>", "__")
    content = content.replace("<triple_underscore>", "___")
    return content

def trim_spaces_on_specific_markdown(content):
    content = mark_replacement(content)
    for i in range(len(regular_expressions_matrix_for_trimming_spaces)):
        character_on_focus = regular_expressions_matrix_for_trimming_spaces[i]['character']
        problematic_strings_left = re.findall(regular_expressions_matrix_for_trimming_spaces[i]['regular_expression_for_wrong_left'], content)
        problematic_strings_right = re.findall(regular_expressions_matrix_for_trimming_spaces[i]['regular_expression_for_wrong_right'], content)
        problematic_strings = list(set(problematic_strings_left) | set(problematic_strings_right))
        for problematic_string in problematic_strings:
            modified_string = problematic_string
            while True:
                modified_string = modified_string.replace(corrections_for_trimming_spaces[i]['right_space'], character_on_focus)        
                modified_string = modified_string.replace(corrections_for_trimming_spaces[i]['left_space'], character_on_focus)
                if bool(re.search(regular_expressions_matrix_for_trimming_spaces[i]['regular_expression_for_correct'], modified_string)):
                    break
            content = content.replace(problematic_string, modified_string)
#            problematic_strings = re.findall(regular_expressions_matrix_for_trimming_spaces[i]['regular_expression_for_wrong'], content)

    content = mark_recovery(content)
    return content        
