import re
from .nttt_logging import log_replacement
from .utilities import apply_to_every_other_part


def trim_md_tags(md_file_content, logging):
    return apply_to_every_other_part(md_file_content, "```", __trim_md_tags, logging)


def __trim_md_tags(md_file_content, logging):
    lines = md_file_content.split("\n")
    trimmed_lines = []
    for i in range(len(lines)):
        line = lines[i]
        star_count = line.count("*")

        is_list_item = star_count % 2 == 1 and line.lstrip().startswith("*")
        if not is_list_item:
            trimmed_lines.append(__trim_md_tags_in_line(line, logging))
        else:
            star_index = line.index("*")
            next_after_star_index = star_index + 1

            list_marker = line[:next_after_star_index]
            list_item_text = line[next_after_star_index:]

            trimmed_lines.append(list_marker + __trim_md_tags_in_line(list_item_text, logging))

    return '\n'.join(trimmed_lines)


def __trim_md_tags_in_line(s, logging):
    return re.sub(r'(?P<tag>`|_{1,3}|\*{1,3})(?P<content>.+?)(?P=tag)', replacement_builder(logging), s)


def replacement_builder(logging):
    def internal_replacement_builder(matchobj):
        original_text = matchobj.group()
        tag_name = matchobj.group("tag")
        stripped_content = matchobj.group("content").strip()

        replacement_text = "{}{}{}".format(tag_name, stripped_content, tag_name)
        log_replacement(original_text, replacement_text, logging)
        return replacement_text

    return internal_replacement_builder
