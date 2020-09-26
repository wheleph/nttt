import re
from .nttt_logging import display_tags


def trim_html_tags(md_file_content, logging):
    # The idea of this loop is to detect text that goes inside backquotes (`) and keep that text unchanged.
    # This is because in Markdown files backquotes enclose code snippets that usually should be not be changed.
    # We achieve this by splitting the content by backquotes and applying html trimming to every other part.
    parts = md_file_content.split("`")
    trimmed_parts = []
    for i in range(len(parts)):
        if (i % 2) == 0:
            trimmed_parts.append(__trim_html_tags(parts[i], logging))
        else:
            trimmed_parts.append(parts[i])

    return '`'.join(trimmed_parts)


def __trim_html_tags(s, logging):
    return re.sub(r'<(?P<tag>[\w\d]+?)>(?P<content>.+?)</(?P=tag)>', replacement_builder(logging), s)


def replacement_builder(logging):
    def internal_replacement_builder(matchobj):
        tag_name = matchobj.group("tag")
        stripped_content = matchobj.group("content").strip()
        if logging == "on":
            display_tags(tag_name, matchobj.group("content"), stripped_content)
        return "<{}>{}</{}>".format(tag_name, stripped_content, tag_name)

    return internal_replacement_builder