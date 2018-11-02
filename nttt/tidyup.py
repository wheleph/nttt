from .utilities import find_files, find_replace, find_snippet

import os
import os.path
from pathlib import Path

def fix_meta(src, dst):
    find_replace(src, dst, "  - \r\n    title:", "  - title:")

def fix_step(src, dst):
    find_replace(src, dst, "\---", "---")
    find_replace(dst, dst, "--- hints ---", "--- hints ---\r\n")
    find_replace(dst, dst, " --- hint --- ", "--- hint ---\r\n")
    find_replace(dst, dst, " --- /hint ---", "\r\n--- /hint ---\r\n")
    find_replace(dst, dst, " --- /hints ---", "--- /hints ---")
    find_replace(dst, dst, '{: target = " blank"}', '{:target="blank"}')
    find_replace(dst, dst, "\n` ", "\n`")

    collapse_error = "--- collapse ---\r\n\r\n* * *\r\n\r\n## title: "
    collapse_title = find_snippet(dst, collapse_error, "\r\n")
    while collapse_title is not None:
        find_replace(dst, dst, collapse_error + collapse_title + "\r\n", "--- collapse ---\r\n---\r\ntitle: " + collapse_title + "\r\n---\r\n")
        collapse_title = find_snippet(dst, collapse_error, "\r\n")

    # doesnt work...  needs thinking about!
    # bold_text = find_snippet(dst, "** ", " **")
    # while bold_text is not None:
    #     find_replace(dst, dst, "** " + bold_text + " **", "**" + bold_text + "**")
    #     bold_text = find_snippet(dst, "** ", " **")


def tidyup_translations(folder, output_folder):

    if os.path.isdir(folder):

        # get absolute paths
        folder = Path(folder).absolute()
        output_folder = Path(output_folder).absolute()

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
                #print(" - {}".format(os.path.basename(file)))
                print(" - {}".format(file.replace(str(folder), "")))
            
            process_yn = input("Continue (y/n):")
            if process_yn.casefold() == "y":

                # create output folder
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)


                for source_file_path in files_to_update:
                    file_name = os.path.basename(source_file_path)
                    output_file_path = os.path.join(output_folder, file_name)
                    print("Fixing - {}".format(file_name))
                    if os.path.basename(source_file_path) == "meta.yml":
                        fix_meta(source_file_path, output_file_path)
                    else:
                        fix_step(source_file_path, output_file_path)
                
                print("Complete")
                    
        else:
            print("No files found in '{}'".format(folder))

    else:
        print("Folder '{}' not found".format(folder))