import re
from .nttt_logging import display_md


def trim_md_tags(md_file_content, logging):
    lines = md_file_content.split("\n")
    trimmed_lines = []
    for i in range(len(lines)):
        line = lines[i]
        star_count = line.count("*")

        is_list_item = star_count % 2 == 1 and line.lstrip().startswith("*")
        if not is_list_item:
            trimmed_lines.append(__trim_md_tags(line, logging))
        else:
            star_index = line.index("*")
            next_after_star_index = star_index + 1

            list_marker = line[:next_after_star_index]
            list_item_text = line[next_after_star_index:]

            trimmed_lines.append(list_marker + __trim_md_tags(list_item_text, logging))

    return '\n'.join(trimmed_lines)


def __trim_md_tags(s, logging):
    return re.sub(r'(?P<tag>`|_{1,3}|\*{1,3})(?P<content>.+?)(?P=tag)', replacement_builder(logging), s)


def replacement_builder(logging):
    def internal_replacement_builder(matchobj):
        tag_name = matchobj.group("tag")
        stripped_content = matchobj.group("content").strip()
        if logging == "on":
            display_md(tag_name, matchobj.group("content"), stripped_content)
        return "{}{}{}".format(tag_name, stripped_content, tag_name)

    return internal_replacement_builder
