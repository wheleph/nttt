import re
filename = 'example.log'

def trim_md_tags(file_content):
    return re.sub(r'(?P<tag>`|_{1,3}|\*{1,3})(?P<content>.+?)(?P=tag)', replacement_builder, file_content)


def replacement_builder(matchobj):
    tag_name = matchobj.group("tag")
    stripped_content = matchobj.group("content").strip()
    if matchobj.group("content") != stripped_content:
        with open(filename, "a") as myfile:
            myfile.write("Tag: {}\n".format(tag_name))
            myfile.write("{}\n".format(matchobj.string))
            myfile.write("{}{}{}\n".format(tag_name, matchobj.group("content"), tag_name))
            myfile.write("{}{}{}\n".format(tag_name, stripped_content, tag_name))
            myfile.write("\n")
    return "{}{}{}".format(tag_name, stripped_content, tag_name)