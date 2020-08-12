import os
import re

#PUB-9 utilities. These methods are for trimming spaces on specific markdown like ** or _. The main method is trim_spaces_on_specific_markdown which uses trim_spaces_on_specific_markdown_breakdown and strings_with_specific_markdown_and_spaces.
 

regular_expressions_matrix_for_trimming_spaces = [
    {'character':'_', 'regular_expression_for_wrong_left':r"_[ ]+[A-Za-z0-9]+[ ]*_", 'regular_expression_for_wrong_right':r"_[ ]*[A-Za-z0-9]+[ ]+_", "regular_expression_for_correct":r"_[A-Za-z0-9]*_"},
    {'character':'`', 'regular_expression_for_wrong_left':r"`[ ]+[A-Za-z0-9]+[ ]*`", 'regular_expression_for_wrong_right':r"`[ ]*[A-Za-z0-9]+[ ]+`", "regular_expression_for_correct":r"`[A-Za-z0-9]*`"},
    {'character':'<double_asterisk>', 'regular_expression_for_wrong_left':r"<double_asterisk>[ ]+[A-Za-z0-9]+[ ]*<double_asterisk>", 'regular_expression_for_wrong_right':r"<double_asterisk>[ ]*[A-Za-z0-9]+[ ]+<double_asterisk>", "regular_expression_for_correct":r"<double_asterisk>[A-Za-z0-9]*<double_asterisk>"},
    {'character':'*', 'regular_expression_for_wrong_left':r"\*[ ]+[A-Za-z0-9]+[ ]*\*", 'regular_expression_for_wrong_right':r"\*[ ]*[A-Za-z0-9]+[ ]+\*", "regular_expression_for_correct":r"\*[A-Za-z0-9]*\*"},
    ]

corrections_for_trimming_spaces = [
    {'character':'_', 'left_space':"_ ", 'right_space':" _"},
    {'character':'`', 'left_space':"` ", 'right_space':" `"},
    {'character':'<double_asterisk>', 'left_space':"<double_asterisk> ", 'right_space':" <double_asterisk>"},
    {'character':'*', 'left_space':"* ", 'right_space':" *"},
    ]

def trim_spaces_on_specific_markdown(content):
    content = content.replace("**", "<double_asterisk>")
    for i in range(4):
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

    content = content.replace("<double_asterisk>", "**")
    return content        
