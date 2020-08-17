import re

# We are using a global variable because the function passed to re.sub() will only get the match as an argument.
# We need another way of knowing the language so that we can enable language specific beahviour.
t_lang = None

def replacement_builder(match):
    """
        Parameters:
            - match -> A Match Object (see re's documentation) containing the matched string.

        Returns:
            A String containing the corrected version of the matched one.

        This function crafts the correct tag from the one containing errors which we've found.
        It's called by re.sub(). It distinguishes between the opening tags (i.e. <foo>) and closing
        tags (i.e </foo>) so that we know how to fix things. It's also language aware so that we may
        treat specific requirements separately like for example the Dutch trailing hypen which has
        already been taken care of. Note we use tha auxiliary variable 'match' so as to avoid calling
        the 'group()' method over and over again so as to reduce the call overhead.
    """

    match = matchobj.group(0)

    if '/' in match:
        if match[-2] != ' ' and ((match[-1] != '-' and t_lang == 'nl-NL') or t_lang != 'nl-NL'):
            match = match[:-1] + ' ' + match[-1]
        if match[1] == ' ':
            match = match[0] + match[1:].lstrip()
    else:
        if match[1] == '<':
            match = match[0] + ' ' + match[1:]
        if match[-2] == ' ':
            match = match[:-1].rstrip() + match[-1]

    return match

def trim_tags(file_content, lang):
    """
        Parameters:
            - file_content -> String containing the current file's content.
            - lang -> String containing the translation's language.

        Returns:
            A String containing the corrected file content.

        This function will just get the file's content, update the global t_lang variable
        and begin finding wrongly formatted tags. It'll then return the corrected file
        content as a string.
    """

    global t_lang
    t_lang = lang

    return re.sub(r'\S\s*</?[\w\d]+>\s*\S', replacement_builder, file_content)