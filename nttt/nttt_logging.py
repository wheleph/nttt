def nttt_display(tag_name, text_before, text_after):
    if text_before != text_after:
        print("Tag name: {}\n".format(tag_name))
        print("Replaced: {}{}{}\n".format(tag_name, text_before, tag_name))
        print("    with: {}{}{}\n".format(tag_name, text_after, tag_name))
    