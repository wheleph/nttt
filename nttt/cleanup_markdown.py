import re
from .nttt_logging import display_md


def trim_md_tags(file_content, logging="off"):
    return re.sub(r'(?P<tag>`|_{1,3}|\*{1,3})(?P<content>.+?)(?P=tag)', replacement_builder(logging), file_content)


def replacement_builder(logging):
    def internal_replacement_builder(matchobj):
        tag_name = matchobj.group("tag")
        stripped_content = matchobj.group("content").strip()
        if logging == "on":
            display_md(tag_name, matchobj.group("content"), stripped_content)
        return "{}{}{}".format(tag_name, stripped_content, tag_name)

    return internal_replacement_builder
