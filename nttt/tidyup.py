import os
import io
import ruamel.yaml
from .acknowledgements import add_volunteer_acknowledgement
from .arguments import get_step_file
from .constants import ArgumentKeyConstants, GeneralConstants
from .utilities import add_missing_entries, find_files, get_file, save_file
from .cleanup_markdown import trim_md_tags
from .cleanup_html import trim_html_tags
from .cleanup_formatting import trim_formatting_tags
from .cleanup_sections import fix_sections
from .cleanup_sections import revert_section_translation


def fix_meta(src, english_src, dst):
    (content, suggested_eol) = get_file(src)
    (english_content, _) = get_file(english_src)

    # Fix steps
    content = content.replace("  - \n    title:", "  - title:")

    # Revert untranslatable elements
    content = revert_untranslatable_meta_elements(content, english_content)

    save_file(dst, content, suggested_eol)


def revert_untranslatable_meta_elements(content, english_content):
    yaml_parser = ruamel.yaml.YAML(typ='rt')
    yaml_parser.preserve_quotes = True
    # Disable timestamp parsing. If enabled it may lead to unwanted errors when the date is invalid.
    # Beware that this approach relies on not documented features. Some details:
    # https://stackoverflow.com/questions/50900727/skip-converting-entities-while-loading-a-yaml-string-using-pyyaml
    yaml_parser.constructor.yaml_constructors.pop(u'tag:yaml.org,2002:timestamp', None)

    parsed_md = yaml_parser.load(content)
    english_parsed_md = yaml_parser.load(english_content)

    translatable_keys = ["title", "description", "steps"]
    for key in parsed_md:
        if key not in translatable_keys and key in english_parsed_md:
            parsed_md[key] = english_parsed_md[key]

    yaml_dumper = ruamel.yaml.YAML()
    yaml_dumper.indent(sequence=4, offset=2)
    yaml_dumper.explicit_start = True
    yaml_dumper.width = 1000000

    string_buffer = io.StringIO()
    yaml_dumper.dump(parsed_md, string_buffer)
    string_buffer.seek(0)
    return string_buffer.read()


def fix_md_step(src, lang, english_src, dst, disable, logging):
    (md_content, suggested_eol) = get_file(src)
    en_md_content = None
    if os.path.isfile(english_src):
        (en_md_content, _) = get_file(english_src)

    if "fix_sections" not in disable:
        md_content = fix_sections(md_content, logging)
        if en_md_content is not None and "revert_section_translation" not in disable:
            md_content = revert_section_translation(src, md_content, en_md_content, logging)

    if "fix_md" not in disable:
        md_content = trim_md_tags(md_content, logging)

    if "fix_html" not in disable:
        md_content = trim_html_tags(md_content, logging)

    if "fix_formatting" not in disable:
        md_content = trim_formatting_tags(md_content, logging)

    # update language in urls
    md_content = md_content.replace("/en/", "/" + lang + "/")

    save_file(dst, md_content, suggested_eol)


def tidyup_translations(arguments):
    input_folder = arguments[ArgumentKeyConstants.INPUT]
    output_folder = arguments[ArgumentKeyConstants.OUTPUT]
    english_folder = arguments[ArgumentKeyConstants.ENGLISH]
    language = arguments[ArgumentKeyConstants.LANGUAGE]
    disable = arguments[ArgumentKeyConstants.DISABLE]
    logging = arguments[ArgumentKeyConstants.LOGGING]
    volunteers = arguments[ArgumentKeyConstants.VOLUNTEERS]
    final_step = arguments[ArgumentKeyConstants.FINAL]
    yes = arguments[ArgumentKeyConstants.YES]

    # get files to update
    print("Find files ...")
    files_to_update = find_files(input_folder, file_names=[GeneralConstants.FILE_NAME_META_YML], extensions=[".md"])

    if len(files_to_update) > 0:
        print("About to tidy up files:")
        for file in files_to_update:
            print(" - {}".format(os.path.relpath(file, input_folder)))

        continue_with_cleanup = True
        if yes != 'on':
            process_yn = input("Continue (y/n):")
            continue_with_cleanup = (process_yn.casefold() == "y")

        if continue_with_cleanup:
            for source_file_path in files_to_update:
                relative_input_file_name = os.path.relpath(source_file_path, input_folder)

                output_file_path = os.path.join(output_folder, relative_input_file_name)

                # create output folder
                output_file_folder = os.path.dirname(output_file_path)

                if not os.path.exists(output_file_folder):
                    os.makedirs(output_file_folder)

                print("Fixing - {}".format(relative_input_file_name))
                en_file_path = os.path.join(english_folder, relative_input_file_name)
                if relative_input_file_name == GeneralConstants.FILE_NAME_META_YML:
                    fix_meta(source_file_path, en_file_path, output_file_path)
                else:
                    fix_md_step(source_file_path, language, en_file_path, output_file_path, disable, logging)

            if final_step > 0:
                output_file_path = get_step_file(output_folder, final_step)
                print("Adding volunteer acknowledgement - {}".format(
                        output_file_path))
                add_volunteer_acknowledgement(
                    GeneralConstants.VOLUNTEER_ACKNOWLEDGEMENTS_CSV,
                    output_file_path, language, volunteers, logging)

            print("Complete")

    else:
        print("No files found in '{}'".format(input_folder))

    # add files and folders missing in the output folder
    add_missing_entries(input_folder, english_folder, output_folder)
