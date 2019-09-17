from .utilities import find_files, find_replace, find_snippet, get_file, save_file

import os
import os.path
import re
from pathlib import Path
import csv
import urllib.request

from .scratchblocks_translate import translate_blocks

HYPERLINK_REGEX = re.compile("\[([^\]]+)\]\s*\(([^\)]+)+\)(?:\s*\{([^\}]+)\})?")
STRONG_REGEX = re.compile("\*{2}(.*?)\*{2}")
EM_REGEX = re.compile("(?<!\*)\*([^*][\w\d\s]+)\*")
INLINE_CODE_REGEX = re.compile("(?<!`)`([^`\n]+)`")
SCRATCH_BLOCK_INLINE_REGEX = re.compile("`([\w\d\s\[\]\(\)]+)`(\s*\{\s*:\s*class\s*=\s*[\"|\'][\w\d\s]+[\"|\']\s*\})")
BULLET_POINT_ASTERISK_REGEX = re.compile("^(\s*)\*(?!\*)(.*)")
BULLET_POINT_PLUS_REGEX = re.compile("^(\s*)\+(.*)")
CODE_BLOCK_OPEN_CLOSE = re.compile("^```")
SOLUTIONS_DIRECTORY = 'solutions'
RESOURCES_DIRECTORY = 'resources'
ACKNOWLEDGEMENTS_CSV_URL = 'https://docs.google.com/spreadsheets/d/1gftThH2QukNPE3C34VINoKmt515eVjhca5cWOQryHNM/export?format=csv'
ACKNOWLEDGEMENTS_CSV_FILE_NAME = 'acknowledgements.csv'

def load_acknowledgements(folder):

    acknowledgements = {}

    file_path = folder / ACKNOWLEDGEMENTS_CSV_FILE_NAME

    with urllib.request.urlopen(ACKNOWLEDGEMENTS_CSV_URL) as response:
        with open(file_path, 'wb') as output:
            data = response.read()
            output.write(data)

    with open(str(file_path), encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:

            acknowledgements[row['Locale']] = row['Text']

    return acknowledgements

def append_acknowledgement_string(last_step_file, acknowledgements):

    lang = os.path.split(os.path.split(last_step_file)[0])[1]

    try:
        content = get_file(last_step_file)
        acknowledgement = acknowledgements[lang]
        content = "{}\n\n{}".format(content, acknowledgement)
        save_file(last_step_file, content)
    except KeyError:
        print("No acknowledgement found for {}.".format(lang))

def fix_hyperlinks(content):
    links = re.finditer(HYPERLINK_REGEX, content)

    replacements = []

    for link in links:

        text = link[1]
        url = link[2]
        target = link[3] if not link[0] == link[3] else None

        text = text.strip()
        url = url.replace(" ", "")

        if target:
            target = target.replace(" ", "")
            new_link = "[{}]({}){{{}}}".format(text, url, target)
        else:
            new_link = "[{}]({})".format(text, url)

        replacements.append((link[0], new_link))

    for replacement in replacements:
        content = content.replace(replacement[0], replacement[1])

    return content

def fix_bullet_points(content):
    elements = re.finditer(BULLET_POINT_ASTERISK_REGEX, content)

    replacements = []

    for element in elements:
        original = element[0]
        fixed = "{}- {}".format(
            element[1],
            element[2].lstrip()
        )

        replacements.append((original, fixed))

    for replacement in replacements:
        content = content.replace(replacement[0], replacement[1])

    elements = re.finditer(BULLET_POINT_PLUS_REGEX, content)

    replacements = []

    for element in elements:
        original = element[0]
        fixed = "{}- {}".format(
            element[1],
            element[2].lstrip()
        )

        replacements.append((original, fixed))

    for replacement in replacements:
        content = content.replace(replacement[0], replacement[1])

    return content


def fix_leading_trailing_spaces_in_tags(content, tag, regex):
    elements = re.finditer(regex, content)

    replacements = []

    for element in elements:
        original = element[0]
        fixed = "{}{}{}".format(
            tag,
            element[1].strip(),
            tag
        )

        replacements.append((original, fixed))

    for replacement in replacements:
        content = content.replace(replacement[0], replacement[1])

    return content


def fix_spaces_in_inline_scratch_blocks(content):
    inline_blocks = re.finditer(SCRATCH_BLOCK_INLINE_REGEX, content)

    replacements = []

    for block in inline_blocks:
        original = block[0]

        block_text = block[1].strip()

        class_text = block[2].replace(" ", "")

        fixed = "`{}`{}".format(block_text, class_text)

        replacements.append((original, fixed))

    for replacement in replacements:
        content = content.replace(replacement[0], replacement[1])

    return content

def fix_file_contents(file_contents):

    in_code_block = False

    content_lines = file_contents.splitlines()

    for i in range(len(content_lines)):

        content = content_lines[i]

        code_block_separator = re.match(CODE_BLOCK_OPEN_CLOSE, content)

        if code_block_separator:

            in_code_block = not in_code_block

        if not in_code_block and not code_block_separator:

            # Fix bullet points to use - character, to avoid confusing subsequent regex with * based bullets
            content = fix_bullet_points(content)

            # Fix inline code tags leading and trailing spaces
            content = fix_leading_trailing_spaces_in_tags(content, "`", INLINE_CODE_REGEX)

            # Fix inline scratchblocks to remove spaces
            content = fix_spaces_in_inline_scratch_blocks(content)

            # Find code inline and remove it, replacing it with placeholders
            inline_code = re.finditer(INLINE_CODE_REGEX, content)

            replaced_code = []

            replaced_code_counter = 0

            for code_snippet in inline_code:
                replaced_code.append(code_snippet[0])
                content = content.replace(
                    replaced_code[replaced_code_counter],
                    '@#!{}!#@'.format(str(replaced_code_counter))
                    )
                replaced_code_counter += 1

            # Fix hyperlinks
            content = fix_hyperlinks(content)

            # Fix strong tags leading and trailing spaces
            content = fix_leading_trailing_spaces_in_tags(content, "**", STRONG_REGEX)

            # Fix em tags leading and trailing spaces
            content = fix_leading_trailing_spaces_in_tags(content, "*", EM_REGEX)

            # Restore the inline code
            for j in range(replaced_code_counter):
                replacement_code = replaced_code[j]

                content = content.replace(
                    '@#!{}!#@'.format(j),
                    replacement_code
                )

            content_lines[i] = content

        i += 1

    return '\n'.join(content_lines) + '\n'

def fix_meta(src, dst):
    find_replace(src, dst, "  - \r\n    title:", "  - title:")

def fix_step(src, dst):
    content = get_file(src)
    content = content.replace("\---", "---")
    content = content.replace("## ---", "---")
    content = content.replace("--- hints ---", "--- hints ---\r\n")
    content = content.replace(" --- hint x--- ", "--- hint ---\r\n")
    content = content.replace(" --- /hint ---", "\r\n--- /hint ---\r\n")
    content = content.replace(" --- /hints ---", "--- /hints ---")
    content = content.replace('{: target = " blank"}', '{:target="blank"}')
    content = content.replace("\n` ", "\n`")
    
    collapse_error = "--- collapse ---\r\n\r\n## title: "
    collapse_title = find_snippet(content, collapse_error, "\r\n")
    while collapse_title is not None:
        content = content.replace(collapse_error + collapse_title + "\r\n", "--- collapse ---\r\n---\r\ntitle: " + collapse_title + "\r\n---\r\n")
        collapse_title = find_snippet(content, collapse_error, "\r\n")

    # update language in urls
    lang = os.path.split(os.path.split(src)[0])[1]
    content = content.replace("/en/", "/" + lang + "/")

    content = fix_file_contents(content)

    save_file(dst, content)

    # doesnt work...  needs thinking about!
    # bold_text = find_snippet(dst, "** ", " **")
    # while bold_text is not None:
    #     find_replace(dst, dst, "** " + bold_text + " **", "**" + bold_text + "**")
    #     bold_text = find_snippet(dst, "** ", " **")


def tidyup_translations(folder, output_folder):

    # tidy up and get absolute paths
    folder = folder.strip().rstrip(os.pathsep).rstrip('"')
    folder = Path(folder).absolute()
    output_folder = output_folder.strip().rstrip(os.pathsep).rstrip('"')
    output_folder = Path(output_folder).absolute()

    if os.path.isdir(folder):

        translator_acknowledgements = load_acknowledgements(folder)

        # get files to update
        if folder == output_folder:
            print("Using folder - {}".format(folder))
        else:
            print("Input folder - '{}'".format(folder))
            print("Output folder - '{}'".format(output_folder))
    
        print("Find files ...")
        files_to_update = find_files(folder, file_names=["meta.yml"], extensions=[".md"])

        if len(files_to_update) > 0:
            print("About to tidy up files:")
            for file in files_to_update:
                print(" - {}".format(file.replace(str(folder), "")))
            
            process_yn = input("Continue (y/n):")
            if process_yn.casefold() == "y":

                steps_by_numbers = {}

                for source_file_path in files_to_update:
                    file_name = source_file_path.replace(str(folder), "")

                    output_file_path = str(output_folder) + file_name
                    
                    # create output folder
                    output_file_folder = os.path.dirname(output_file_path)


                    if not os.path.exists(output_file_folder):
                        os.makedirs(output_file_folder)

                    print("Tidying {}".format(file_name.lstrip('/').lstrip('\\')))
                    if os.path.basename(source_file_path) == "meta.yml":
                        fix_meta(source_file_path, output_file_path)
                    else:
                        fix_step(source_file_path, output_file_path)
                        if file_name.startswith('/step_') or file_name.startswith('\step_'):
                            step_number = file_name[6:-3]
                            steps_by_numbers[step_number] = output_file_path

                max_step_number = max(steps_by_numbers.keys())

                append_acknowledgement_string(steps_by_numbers[max_step_number], translator_acknowledgements)

                if os.path.exists(folder / ACKNOWLEDGEMENTS_CSV_FILE_NAME):
                    os.remove(folder / ACKNOWLEDGEMENTS_CSV_FILE_NAME)


            # Check for resources directory and create if absent

            resource_path = folder.joinpath(RESOURCES_DIRECTORY)

            if not (
                        os.path.isdir(resource_path) and os.path.exists(resource_path)
            ):
                os.makedirs(resource_path)

            resource_placeholder_file = resource_path.joinpath('.keep')

            if not os.path.exists(resource_placeholder_file):
                with open(resource_placeholder_file, 'w'): pass

            # Check for solutions directory and create if absent

            solutions_path = folder.joinpath(SOLUTIONS_DIRECTORY)

            if not (
                        os.path.isdir(solutions_path) and os.path.exists(solutions_path)
            ):
                os.makedirs(solutions_path)

            solutions_placeholder_file = solutions_path.joinpath('.keep')

            if not os.path.exists(solutions_placeholder_file):
                with open(solutions_placeholder_file, 'w'): pass

                
            print("About to translate scratchblocks:")

            translate_scratchblocks_yn = input("Continue (y/n):")

            if translate_scratchblocks_yn.casefold() == "y":

                target_folder = folder
                target_language = str(os.path.split(target_folder)[1]).split('-')[0]

                translate_blocks(target_folder, target_language)

                print("Translated scratchblocks")

            print("Complete")
                    
        else:
            print("No files found in '{}'".format(folder))

    else:
        print("Folder '{}' not found".format(folder))