def log_replacement(text_before, text_after, logging):
    if logging == "on" and text_before != text_after:
        print("Replaced: {}".format(text_before))
        print("    with: {}".format(text_after))
