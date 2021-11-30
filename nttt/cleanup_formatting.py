import re
from .nttt_logging import log_replacement
from .constants import RegexConstants

pattern_blank = re.compile(rf'^_[{RegexConstants.SPACES}]+blank$')


def trim_formatting_tags(md_file_content, logging):
    s = f"[{RegexConstants.SPACES}]"
    c = f"[{RegexConstants.COLONS}]"
    q = f"[{RegexConstants.QUOTES}]"
    return re.sub(rf'(?P<last_word>\S+?){s}*{{{s}*{c}{s}*(?P<tag>[\w]+?){s}*={s}*{q}{s}*(?P<value>.+?){s}*{q}{s}*}}',
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
