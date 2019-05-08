import codecs
import os.path
from re import match, split
from time import sleep
from urllib.parse import quote, urlparse, parse_qs, unquote

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

SCRATCHBLOCKS_TRANSLATION_URL = "https://scratchblocks.github.io/translator/#?lang={}&script={}"

# The DOM ID of the element containing the translated output on the scratchblocks webpage
# Note that we have to pull it from the href of this link as it's not readily accessable from the textbox
OUTPUT_ELEMENT_ID = "home-link-2"

OUTPUT_CODE_QUERY_PARAM = "script"

TRANSLATIONS_DIRECTORY = "scratchblocks-translations"

CODE_START_INDICATOR_MARKDOWN = ["```blocks3"]

CODE_END_INDICATOR_MARKDOWN = ["```"]

LEADING_CHARACTERS_REGEX = "^[ +-]+"


# Create a selenium browser instance
def create_selenium_chrome_browser():
    browser_options = Options()
    browser = Chrome(options=browser_options)

    return browser


# Find files with any of the provided extensions in a given directory
def find_files(directory, file_extensions=[]):
    found_files = []

    # Get a list of all the files in the directory, and any child directories
    # Iterate over them and check for matches to the listed extensions

    if len(file_extensions) == 0:
        return file_extensions

    for root, directories, filenames in os.walk(directory):

        for filename in filenames:

            file_path = os.path.join(root, filename)

            file_extension = os.path.splitext(file_path)[1][1:]

            if file_extension in file_extensions:
                found_files.append(file_path)

    return found_files


# Build project directory
def get_project_directory(base_directory, repository_name):
    return os.path.join(base_directory, repository_name)


# Build language directory within project
def get_language_directory(project_directory, language_code):
    return os.path.join(project_directory, language_code)


# Get markdown files from project
def get_markdown_files(language_directory):
    return find_files(language_directory, ["md"])


# Get the code blocks from inside a markdown file
def get_code_blocks_from_markdown_file(file_path):
    # The blocks of code without their surrounding markdown, for uploading to the translator
    code_blocks = []

    # The blocks of code with their surrounding markdown, for storing away
    markdown_blocks = []

    # Boolean to track if we're inside a code block as we iterate over the code line-by-line
    in_code_block = False

    # Temporary strings to hold the markdown and code blocks as they are built
    current_code_block = ""

    current_markdown_block = ""

    with codecs.open(file_path, encoding='utf-8') as file:

        # Look for the markdown indicators of a code block starting
        for line in file.readlines():

            clean_line = line.strip().replace(" ", "")

            if clean_line in CODE_START_INDICATOR_MARKDOWN:
                in_code_block = True

                # Start a new markdown block
                current_markdown_block = line

                # Empty the temp code block out
                current_code_block = ""

            elif clean_line in CODE_END_INDICATOR_MARKDOWN and in_code_block:

                current_markdown_block += line

                markdown_blocks.append(current_markdown_block)

                code_blocks.append(current_code_block)

                in_code_block = False

            elif in_code_block:

                current_markdown_block += line

                current_code_block += line

    return code_blocks, markdown_blocks


# Clean code for translation and return a matching list of addition/removal markers and line numbers
def strip_modification_markers(code):
    code_list = code.split("\n")

    modifier_characters = []

    for line_number in range(0, len(code_list) - 1):
        modifiers_on_line = match(LEADING_CHARACTERS_REGEX, code_list[line_number])

        modifiers = modifiers_on_line.group(0) if modifiers_on_line else ""

        modifier_characters.append(modifiers)

        code_list[line_number] = code_list[line_number][len(modifiers):]

    return "\n".join(code_list), modifier_characters


# Restore the modifier characters to code, for use post-translation
def restore_modification_markers(code, modifier_characters):
    code_list = code.split("\n")

    # Cover for an un-closed loop by adding some spaces to the modifiers:
    if len(modifier_characters) == len(code_list) - 1:
        proxy_modifier = split(modifier_characters[0], "+ | -")[-1]

        modifier_characters.append(proxy_modifier)

    for line_number in range(0, len(code_list)):
        code_list[line_number] = "{}{}".format(modifier_characters[line_number], code_list[line_number])

    return "\n".join(code_list)


# Get translations from the web
def fetch_translated_code(browser, english_code, target_language_iso_code):
    # Make the code URL safe
    url_safe_code = quote(english_code)

    # Construct destination URL for translation page
    destination_url = SCRATCHBLOCKS_TRANSLATION_URL.format(target_language_iso_code, url_safe_code)

    browser.get(destination_url)

    sleep(2)

    output_link = browser.find_element_by_id(OUTPUT_ELEMENT_ID).get_attribute("href")

    parsed_output_link = urlparse(output_link)

    return unquote(parse_qs(parsed_output_link.fragment)[OUTPUT_CODE_QUERY_PARAM][0])


def make_directory(directory_path):
    try:
        os.mkdir(directory_path)
    except OSError:
        print("Creation of directory %s failed" % directory_path)


def make_translation_directories(base_language_directory):
    # Create translations directory inside language directory
    block_translations_directory = os.path.join(base_language_directory, TRANSLATIONS_DIRECTORY)

    make_directory(block_translations_directory)

    # Create a folder for the en blocks and a folder for the translated blocks inside that

    source_blocks = os.path.join(block_translations_directory, "original")

    translated_blocks = os.path.join(block_translations_directory, "translated")

    make_directory(source_blocks)

    make_directory(translated_blocks)

    return {"source": source_blocks, "translated": translated_blocks}


def make_code_file(parent_directory, file_name, contents):
    file_path = os.path.join(parent_directory, file_name)

    with open(file_path, "w") as file:
        file.write(contents)


def file_find_replace(file_path, text_pairs=[]):
    with open(file_path, "r") as file:
        file_text = file.read()

    for pair in text_pairs:
        file_text = file_text.replace(pair[0], pair[1])

    with open(file_path, "w") as file:
        file.write(file_text)


def get_markdown_filename(filepath, language_directory, snippet_number):
    filename = str(filepath).replace(str(language_directory), "")

    output_filename = filename.replace(".md", "").replace("/", "__")

    return "{}_block_{}.txt".format(output_filename, snippet_number)


# Main translation method

def translate_blocks(language_directory, language):
    translation_directories = make_translation_directories(language_directory)

    files = get_markdown_files(language_directory)

    my_browser = create_selenium_chrome_browser()

    for file_number in range(0, len(files)):

        blocks = get_code_blocks_from_markdown_file(files[file_number])

        code = blocks[0]
        markdown = blocks[1]

        translated_pairs = []

        for snippet_number in range(0, len(code)):
            cleared_markers = strip_modification_markers(code[snippet_number])

            translation = fetch_translated_code(my_browser, cleared_markers[0], language)

            source_markdown = markdown[snippet_number]

            markdown_list = source_markdown.split("\n")

            translated_markdown = "{}\n{}\n{}\n".format(
                markdown_list[0],
                restore_modification_markers(
                    translation,
                    cleared_markers[1]
                ),
                markdown_list[-2]
            )

            markdown_filename = get_markdown_filename(files[file_number], language_directory, snippet_number)

            make_code_file(
                translation_directories["source"],
                markdown_filename,
                source_markdown
            )

            make_code_file(
                translation_directories["translated"],
                markdown_filename,
                translated_markdown
            )

            translated_pairs.append((source_markdown, translated_markdown))

        # Find/replace in original file
        file_find_replace(files[file_number], translated_pairs)

    my_browser.close()
