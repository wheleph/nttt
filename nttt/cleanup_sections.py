import re
import sys
from .utilities import find_snippet
from .nttt_logging import log_replacement


def fix_sections(md_file_content, logging):
    # For some weird reason Crowdin replaces '---' to '\---' in its output. So let's revert it back
    md_file_content = md_file_content.replace("\\---", "---")

    # Fixes 2 issues:
    # - users could mistakenly remove one dash
    # - users could mistakenly remove spaces around the tag
    md_file_content = re.sub(r'---?[ \t]*(?P<tag>.+?)[ \t]*---?',
                             replacement_builder(logging, "--- {} ---"),
                             md_file_content)

    # For some weird reason Crowdin jams 'hints' and 'hint' tags into one line it its output.
    # So "--- hints ---\n--- hint ---" becomes "--- hints --- --- hint ---".
    # Probably because they go in adjacent lines (no empty line between them).
    # So let's revert it back (also considering situations when translators mistakenly
    # modified those strings, for example translated them in target language
    md_file_content = re.sub(r'--- (?P<tag>.+?) ---[ \t]+(?=--- .+? ---)',
                             replacement_builder(logging, "--- {} ---\n"),
                             md_file_content)

    # For some weird reason Crowdin breaks 'title' tags. So let's revert it back
    collapse_error = "## --- collapse ---\n\n## title: "
    collapse_title = find_snippet(md_file_content, collapse_error, "\n")
    while collapse_title is not None:
        original_text = collapse_error + collapse_title + "\n"
        replacement_text = "--- collapse ---\n---\ntitle: " + collapse_title + "\n---\n"
        md_file_content = md_file_content.replace(original_text, replacement_text)
        log_replacement(original_text, replacement_text, logging)

        collapse_title = find_snippet(md_file_content, collapse_error, "\n")

    return md_file_content


def replacement_builder(logging, replacement_pattern):
    def internal_replacement_builder(matchobj):
        original_text = matchobj.group()
        tag_name = matchobj.group("tag")

        replacement_text = replacement_pattern.format(tag_name)
        log_replacement(original_text, replacement_text, logging)
        return replacement_text

    return internal_replacement_builder


def fix_sections_translation(md_file_name, md_file_content, en_file_content, logging):
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
