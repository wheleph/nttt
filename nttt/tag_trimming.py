import re
from .nttt_logging import display_tags


def trim_tags(file_content, logging):
    return re.sub(r'<(?P<tag>[\w\d]+?)>(?P<content>.+?)</(?P=tag)>', replacement_builder(logging), file_content)


def replacement_builder(logging):
    def internal_replacement_builder(matchobj):
        tag_name = matchobj.group("tag")
        stripped_content = matchobj.group("content").strip()
        if logging == "on":
            display_tags(tag_name, matchobj.group("content"), stripped_content)
        return "<{}>{}</{}>".format(tag_name, stripped_content, tag_name)

    return internal_replacement_builder