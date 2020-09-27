import os, yaml
from .constants import ArgumentKeyConstants, GeneralConstants
from .utilities import add_missing_entries, find_files, find_snippet, get_file, save_file
from .cleanup_markdown import trim_md_tags
from .cleanup_html import trim_html_tags


def fix_meta(src, english_src, dst):
    (content, suggested_eol) = get_file(src)
    (english_content, _) = get_file(english_src)

    # Fix steps
    content = content.replace("  - \n    title:", "  - title:")

    # Revert untranslatable elements
    content = revert_untranslatable_meta_elements(content, english_content)

    save_file(dst, content, suggested_eol)


def revert_untranslatable_meta_elements(content, english_content):
    parsed_md = yaml.safe_load(content)
    english_parsed_md = yaml.safe_load(english_content)

    translatable_keys = ["title", "description", "steps"]
    for key in parsed_md:
        if key not in translatable_keys:
            parsed_md[key] = english_parsed_md[key]

    class IndentedDumper(yaml.Dumper):
        """
        There are different ways to print sequence elements in YAML. They may or may not be indented.
        This class is needed to make the indented (to preserve existing behaviour of the program).
        See https://stackoverflow.com/a/39681672/15647 for more details
        """
        def increase_indent(self, flow=False, indentless=False):
            return super(IndentedDumper, self).increase_indent(flow, False)

    return '---\n' + yaml.dump(parsed_md,
                               Dumper=IndentedDumper,
                               allow_unicode=True,
                               sort_keys=False,
                               width=1000000)


def fix_md_step(src, lang, dst, disable, logging):
    md_content, suggested_eol = get_file(src)
    md_content = md_content.replace("\---", "---")
    md_content = md_content.replace("## ---", "---")
    md_content = md_content.replace("--- hints ---", "--- hints ---\n")
    md_content = md_content.replace(" --- hint --- ", "--- hint ---\n")
    md_content = md_content.replace(" --- /hint ---", "\n--- /hint ---\n")
    md_content = md_content.replace(" --- /hints ---", "--- /hints ---")
    md_content = md_content.replace('{: target = " blank"}', '{:target="blank"}')
    md_content = md_content.replace("\n` ", "\n`")

    if "fix_md" not in disable:
        md_content = trim_md_tags(md_content, logging)

    if "fix_html" not in disable:
        md_content = trim_html_tags(md_content, logging)

    collapse_error = "--- collapse ---\n\n## title: "
    collapse_title = find_snippet(md_content, collapse_error, "\n")
    while collapse_title is not None:
        md_content = md_content.replace(collapse_error + collapse_title + "\n", "--- collapse ---\n---\ntitle: " + collapse_title + "\n---\n")
        collapse_title = find_snippet(md_content, collapse_error, "\n")

    # update language in urls
    md_content = md_content.replace("/en/", "/" + lang + "/")

    save_file(dst, md_content, suggested_eol)

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
    disable = arguments[ArgumentKeyConstants.DISABLE]
    logging = arguments[ArgumentKeyConstants.LOGGING]
    # volunteers = arguments[ArgumentKeyConstants.VOLUNTEERS]
    # final_step = arguments[ArgumentKeyConstants.FINAL]

    # get files to update
    print("Find files ...")
    files_to_update = find_files(folder, file_names=[GeneralConstants.FILE_NAME_META_YML], extensions=[".md"])

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
                if os.path.basename(source_file_path) == GeneralConstants.FILE_NAME_META_YML:
                    fix_meta(source_file_path, os.path.join(english_folder, GeneralConstants.FILE_NAME_META_YML), output_file_path)
                else:
                    fix_md_step(source_file_path, language, output_file_path, disable, logging)

            print("Complete")

    else:
        print("No files found in '{}'".format(folder))

    # add files and folders missing in the output folder
    add_missing_entries(folder, english_folder, output_folder)
