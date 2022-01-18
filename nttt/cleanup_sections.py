import re
import sys
from .nttt_logging import log_replacement
from .constants import RegexConstants


section_tag_name_regex = f'/?\\w+(?:[\\-{RegexConstants.SPACES}]\\w+)*'


def fix_sections(md_file_content, logging):
    # For some weird reason Crowdin replaces '---' to '\---' in its output. So let's revert it back
    md_file_content = md_file_content.replace("\\---", "---")

    s = f"[{RegexConstants.SPACES}]"

    # Fixes 2 issues:
    # - users could mistakenly remove one dash
    # - users could mistakenly remove spaces around the tag
    md_file_content = re.sub(rf'---?{s}*(?P<tag>{section_tag_name_regex}?){s}*---?',
                             replacement_builder(logging, ["tag"], "--- {} ---"),
                             md_file_content)

    # Removes any possible spaces between '/' and tag name in closing tags
    md_file_content = re.sub(rf'--- /{s}+(?P<tag>{section_tag_name_regex}?) ---',
                             replacement_builder(logging, ["tag"], "--- /{} ---"),
                             md_file_content)

    # For some weird reason Crowdin jams 'hints' and 'hint' tags into one line it its output.
    # So "--- hints ---\n--- hint ---" becomes "--- hints --- --- hint ---".
    # Probably because they go in adjacent lines (no empty line between them).
    # So let's revert it back (also considering situations when translators mistakenly
    # modified those strings, for example translated them in target language
    md_file_content = re.sub(rf'--- (?P<tag>{section_tag_name_regex}?) ---{s}+(?=.+)',
                             replacement_builder(logging, ["tag"], "--- {} ---\n"),
                             md_file_content)
    md_file_content = re.sub(rf'(?P<content>\S+?){s}+--- (?P<tag>{section_tag_name_regex}?) ---',
                             replacement_builder(logging, ["content", "tag"], "{}\n--- {} ---"),
                             md_file_content)

    # For some weird reason Crowdin breaks 'title' tags. So let's revert it back
    c = f"[{RegexConstants.COLONS}]"
    md_file_content = re.sub(rf'##\n--- collapse ---\n\n## (?P<tag>.+?){c}{s}*(?P<title>.+?)\n',
                             replacement_builder(logging, ["title"], "--- collapse ---\n---\ntitle: {}\n---\n"),
                             md_file_content)

    return md_file_content


def replacement_builder(logging, groups_to_extract, replacement_pattern):
    def internal_replacement_builder(matchobj):
        original_text = matchobj.group()
        group_values = [matchobj.group(group_name) for group_name in groups_to_extract]

        replacement_text = replacement_pattern.format(*group_values)
        log_replacement(original_text, replacement_text, logging)
        return replacement_text

    return internal_replacement_builder


def revert_section_translation(md_file_name, md_file_content, en_file_content, logging):
    """
    Compares translated file to the original one
    and reverts translated section tags ("--- opdracht ---" -> "--- task ---").
    This happens if both the original file and the translated one contain the same number of those tags
    """
    section_pattern = re.compile("--- (?P<tag>.+?) ---")

    md_file_lines = md_file_content.split('\n')
    md_file_section_dict = extract_sections(md_file_lines, section_pattern)

    en_file_lines = en_file_content.split('\n')
    en_file_section_dict = extract_sections(en_file_lines, section_pattern)

    if len(md_file_section_dict) == len(en_file_section_dict):
        md_sec_line_num = sorted(md_file_section_dict)
        en_sec_line_num = sorted(en_file_section_dict)

        for i in range(len(md_sec_line_num)):
            idx_section_to_replace = md_sec_line_num[i]
            replacement_text = en_file_section_dict[en_sec_line_num[i]]

            log_replacement(md_file_lines[idx_section_to_replace], replacement_text, logging)
            md_file_lines[idx_section_to_replace] = replacement_text

        return '\n'.join(md_file_lines)
    else:
        print("Warning ({}): Different section structure in the original (en) and the translated pages. "
              "Reverting of translated section tags will not be performed".format(md_file_name), file=sys.stderr)
        return md_file_content


# return dictionary of the following structure:
# line number -> section text (i. e.: 0 -> "--- hints ---")
def extract_sections(md_file_lines, section_pattern):
    sections = {}

    for i in range(len(md_file_lines)):
        line = md_file_lines[i]
        if section_pattern.match(line):
            sections[i] = line

    return sections
