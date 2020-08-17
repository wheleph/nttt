import re

# We are using a global variable because the function passed to re.sub() will only get the match as an argument.
# We need another way of knowing the language so that we can enable language specific beahviour.
t_lang = None

# This list holds the locales identifying languages whose trailing hypens should be treated differently.
hypen_langs = [
    'nl-NL'
]

# REs
IN_TEXT_TAG = "\S\s*</?[\w\d]+>\s*\S"
BEGINNING_TAG = "^<[\w\d]+>\s+\S"
ENDING_TAG = "\S\s+</[\w\d]+>"

def replacement_builder(matchobj):
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

        Note the second check on line 28 accounts for the case where we have trailing closing tags.
    """

    match = matchobj.group(0)

    if '/' in match:
        if match[-2] != ' ' and match[-1] != '>' and ((match[-1] != '-' and t_lang in hypen_langs) or t_lang not in hypen_langs):
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

        Description:
            This function will just get the file's content, update the global t_lang variable
            and begin finding wrongly formatted tags. It'll then return the corrected file
            content as a string.

        RE Summary:
            - IN_TEXT_TAG -> It will extrac wrong tags that are followed and preceded by text.
            - BEGINNING_TAG -> It will extract opening tags at the beginning of a line.
            - ENDING_TAG -> It will extract closing tags at the end of a line.

        RE Notes:
            The OR operator (|) is NOT greedy in that if there's a match for the first RE we'll
            call replacement_builder() right away. That's why the latter two REs are intended
            for weirder scenarios. At the moment they are just in place for passing "synthetic"
            unit tests we have prepared. We expect tags to always be surounded by a charcter,
            be it a dot or the beginning of a sentence. If we were to end a line on a tag we
            could just use [\S$] instead of just \S in IN_TEXT_TAG so as to have one les RE.

            Declaring the REs as global variables could allow other scripts to import them
            may it be needed.
    """

    global t_lang
    t_lang = lang

    return re.sub(r'{}|{}|{}'.format(
                                        IN_TEXT_TAG,
                                        BEGINNING_TAG,
                                        ENDING_TAG
                                    ),
                    replacement_builder,
                    file_content)