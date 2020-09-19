import re
from .nttt_logging import nttt_display


def trim_tags(file_content):
    return re.sub(r'<(?P<tag>[\w\d]+?)>(?P<content>.+?)</(?P=tag)>', replacement_builder, file_content)


def replacement_builder(matchobj):
    tag_name = matchobj.group("tag")
    stripped_content = matchobj.group("content").strip()
    nttt_display(tag_name, matchobj.group("content"), stripped_content)
    return "<{}>{}</{}>".format(tag_name, stripped_content, tag_name)