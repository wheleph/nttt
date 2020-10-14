import re
from .nttt_logging import display_tags
from .utilities import apply_to_every_other_part


def trim_html_tags(md_file_content, logging):
    # The idea of this loop is to detect text that goes inside backquotes (`) and keep that text unchanged.
    # This is because in Markdown files backquotes enclose code snippets that usually should be not be changed.
    # We achieve this by splitting the content by backquotes and applying html trimming to every other part.
    # Due to rather lucky coincidence this code also takes care of not changing content inside triple backquotes (```)
    return apply_to_every_other_part(md_file_content, "`", __trim_html_tags, logging)


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
