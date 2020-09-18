import re
filename = 'example.log'

def trim_md_tags(file_content):
    return re.sub(r'(?P<tag>`|_{1,3}|\*{1,3})(?P<content>.+?)(?P=tag)', replacement_builder, file_content)


def replacement_builder(matchobj):
    tag_name = matchobj.group("tag")
    stripped_content = matchobj.group("content").strip()
    if matchobj.group("content") != stripped_content:
        with open(filename, "a", encoding='utf-8') as myfile:
            myfile.write("Tag name: {}\n".format(tag_name))
            myfile.write("Replaced: {}{}{}\n".format(tag_name, matchobj.group("content"), tag_name))
            myfile.write("    with: {}{}{}\n".format(tag_name, stripped_content, tag_name))
    return "{}{}{}".format(tag_name, stripped_content, tag_name)
