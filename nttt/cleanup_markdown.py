import re


def trim_md_tags(file_content):
    return re.sub(r'(?P<tag>`|_{1,3}|\*{1,3})(?P<content>.+?)(?P=tag)', replacement_builder, file_content)


def replacement_builder(matchobj):
    tag_name = matchobj.group("tag")
    stripped_content = matchobj.group("content").strip()
    return "{}{}{}".format(tag_name, stripped_content, tag_name)