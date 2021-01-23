import re
from .nttt_logging import log_replacement

pattern_blank = re.compile(r'^_\s+blank$')


def trim_formatting_tags(md_file_content, logging):
    return re.sub(r'(?P<last_word>\S+?)\s*{\s*[:：]\s*(?P<tag>[\w]+?)\s*=\s*["”“]\s*(?P<value>.+?)\s*["”“]\s*}',
                  replacement_builder(logging),
                  md_file_content)


def replacement_builder(logging):
    def internal_replacement_builder(matchobj):
        original_text = matchobj.group()
        last_word = matchobj.group("last_word")
        tag_name = matchobj.group("tag").lower()
        value = matchobj.group("value").lower()

        if pattern_blank.match(value):
            value = "_blank"

        replacement_text = '{}{{:{}="{}"}}'.format(last_word, tag_name, value)
        log_replacement(original_text, replacement_text, logging)
        return replacement_text

    return internal_replacement_builder
