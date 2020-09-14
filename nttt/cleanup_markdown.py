import re
import logging
logging.basicConfig(filename='example.log',level=logging.INFO)


def trim_md_tags(file_content):
    myregex = r'(?P<tag>`|_{1,3}|\*{1,3})(?P<content>.+?)(?P=tag)'
    result = re.sub(myregex, replacement_builder, file_content)
    delta = re.findall(myregex, file_content)
    delta2 = ['{0}{1}{0}'.format(i[0], i[1]) for i in delta]
    delta3 = [re.sub(myregex, replacement_builder, i) for i in delta2]
    for i, j in zip(delta2, delta3):
        logging.info('New substitution')
        logging.info(i)
        logging.info(j)
    return result


def replacement_builder(matchobj):
    tag_name = matchobj.group("tag")
    stripped_content = matchobj.group("content").strip()
    return "{}{}{}".format(tag_name, stripped_content, tag_name)