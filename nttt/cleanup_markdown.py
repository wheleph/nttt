import re
from .nttt_logging import nttt_display

def trim_md_tags(file_content, logging):
    if logging == "off":
        return re.sub(r'(?P<tag>`|_{1,3}|\*{1,3})(?P<content>.+?)(?P=tag)', replacement_builder, file_content)
    elif logging == "on":
        return re.sub(r'(?P<tag>`|_{1,3}|\*{1,3})(?P<content>.+?)(?P=tag)', replacement_builder_logging, file_content)


def replacement_builder(matchobj):
    tag_name = matchobj.group("tag")
    stripped_content = matchobj.group("content").strip()
    return "{}{}{}".format(tag_name, stripped_content, tag_name)

def replacement_builder_logging(matchobj):
    tag_name = matchobj.group("tag")
    stripped_content = matchobj.group("content").strip()
    nttt_display(tag_name, matchobj.group("content"), stripped_content)
    return "{}{}{}".format(tag_name, stripped_content, tag_name)