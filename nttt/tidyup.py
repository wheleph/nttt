from .constants import ArgumentKeyConstants
from nttt.project import add_missing_entries
from .utilities import find_files, find_replace, find_snippet, get_file, save_file

import os.path


def fix_meta(src, dst):
    find_replace(src, dst, "  - \n    title:", "  - title:")


def fix_step(src, lang, dst):
    content, suggested_eol = get_file(src)
    content = content.replace("\---", "---")
    content = content.replace("## ---", "---")
    content = content.replace("--- hints ---", "--- hints ---\n")
    content = content.replace(" --- hint --- ", "--- hint ---\n")
    content = content.replace(" --- /hint ---", "\n--- /hint ---\n")
    content = content.replace(" --- /hints ---", "--- /hints ---")
    content = content.replace('{: target = " blank"}', '{:target="blank"}')
    content = content.replace("\n` ", "\n`")

    collapse_error = "--- collapse ---\n\n## title: "
    collapse_title = find_snippet(content, collapse_error, "\n")
    while collapse_title is not None:
        content = content.replace(collapse_error + collapse_title + "\n", "--- collapse ---\n---\ntitle: " + collapse_title + "\n---\n")
        collapse_title = find_snippet(content, collapse_error, "\n")

    # update language in urls
    content = content.replace("/en/", "/" + lang + "/")

    save_file(dst, content, suggested_eol)

    # doesnt work...  needs thinking about!
    # bold_text = find_snippet(dst, "** ", " **")
    # while bold_text is not None:
    #     find_replace(dst, dst, "** " + bold_text + " **", "**" + bold_text + "**")
    #     bold_text = find_snippet(dst, "** ", " **")


def tidyup_translations(arguments):

    folder = arguments[ArgumentKeyConstants.INPUT]
    output_folder = arguments[ArgumentKeyConstants.OUTPUT]
    english_folder = arguments[ArgumentKeyConstants.ENGLISH]
    language = arguments[ArgumentKeyConstants.LANGUAGE]
    # volunteers = arguments[ArgumentKeyConstants.VOLUNTEERS]
    # final_step = arguments[ArgumentKeyConstants.FINAL]

    # get files to update
    print("Find files ...")
    files_to_update = find_files(folder, file_names=["meta.yml"], extensions=[".md"])

    if len(files_to_update) > 0:
        print("About to tidy up files:")
        for file in files_to_update:
            print(" - {}".format(file.replace(str(folder), "")))

        process_yn = input("Continue (y/n):")
        if process_yn.casefold() == "y":

            for source_file_path in files_to_update:
                file_name = source_file_path.replace(str(folder), "")

                output_file_path = str(output_folder) + file_name

                # create output folder
                output_file_folder = os.path.dirname(output_file_path)

                if not os.path.exists(output_file_folder):
                    os.makedirs(output_file_folder)

                print("Fixing - {}".format(file_name))
                if os.path.basename(source_file_path) == "meta.yml":
                    fix_meta(source_file_path, output_file_path)
                else:
                    fix_step(source_file_path, language, output_file_path)

            print("Complete")

    else:
        print("No files found in '{}'".format(folder))

    # add files and folders missing in the output folder
    add_missing_entries(folder, english_folder, output_folder)
