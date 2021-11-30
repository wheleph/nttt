import os.path
from pathlib import Path
from shutil import copyfile, copytree
import eol


def get_file(file_name):
    with open(file_name, encoding='utf-8') as f:
        (_, suggested_eol) = eol.eol_info_from_path(file_name)
        return f.read(), suggested_eol


def save_file(file_name, content, suggested_eol):
    with open(file_name, encoding='utf-8', mode="w", newline=suggested_eol) as f:
        f.write(content)


def find_files(src, file_names=[], extensions=[]):
    files_found = []

    for dname, dirs, files in os.walk(src):
        for fname in files:
            fpath = os.path.join(dname, fname)

            # check file_names and extensions
            valid_file = False

            if len(extensions) > 0:
                ext = os.path.splitext(fpath)
                if ext[-1] in extensions:
                    valid_file = True

            if len(file_names) > 0:
                if fname in file_names:
                    valid_file = True

            # if we arent checking file_names or extension it must be valid
            if len(extensions) == 0 and len(file_names) == 0:
                valid_file = True

            if valid_file:
                files_found.append(fpath)

    return sorted(files_found)


def find_missing_entries(source_folder, dest_folder):
    '''
    Returns a list of folders that are present in the source folder, but not in
    the destination folder plus a list of files that are present in the source
    folder, but not in the destination folder.
    Files or folders that are inside a folder from the missing folders list are
    not present in the missing files and folders lists.
    '''

    missing_folders = []
    missing_files = []
    for item in source_folder.iterdir():
        base_item = os.path.basename(item)
        dest_item = Path(dest_folder, base_item)
        if not dest_item.exists():
            if item.is_dir():
                missing_folders.append(base_item)
            elif item.is_file():
                missing_files.append(base_item)

    return (missing_folders, missing_files)


def copy_missing_folders(source_folder, folders_to_copy, dest_folder):
    '''
    Copies the given folders, including contents, from the source folder to the
    destination folder.
    '''
    _copy_missing_items("folder", source_folder, folders_to_copy, copytree, dest_folder)


def copy_missing_files(source_folder, files_to_copy, dest_folder):
    '''
    Copies the given files from the source folder to the destination folder.
    '''
    _copy_missing_items("file", source_folder, files_to_copy, copyfile, dest_folder)


def _copy_missing_items(type_of_items, source_folder, items_to_copy, copy_function, dest_folder):
    '''
    Copies the given items from the source folder to the destination folder,
    using the provided copy function.
    '''

    print("Copying {}s from {} to {}:".format(type_of_items, source_folder, dest_folder))
    for item_to_copy in items_to_copy:
        print(" - {}".format(item_to_copy))

    for item_to_copy in items_to_copy:
        source_path = Path(source_folder, item_to_copy)
        dest_path = Path(dest_folder, item_to_copy)
        copy_function(source_path, dest_path)


def add_missing_entries(input_folder, english_folder, output_folder):
    '''
    Adds missing files and folders to the output folder.

    If the output folder is not the same as the input folder, all files and
    folders in the input folder that are not in the output folder, will be
    copied to the output folder.
    Typically, this will be the images, resources and solutions folders,
    because previous processing steps will have only resulted in a meta.yml
    file and mark-down files in the output folder.

    All folders in the English folder that are not in the output folder, will
    also be copied to the output folder.
    Any file in the English folder that is not in the output folder, will NOT
    be copied to the output folder. The user will have to do this manually.
    '''

    # Start with the input folder, if it is not the same as the output folder.
    if input_folder != output_folder:
        (folders_to_copy, files_to_copy) = find_missing_entries(input_folder, output_folder)
        if len(folders_to_copy) > 0:
            copy_missing_folders(input_folder, folders_to_copy, output_folder)
        if len(files_to_copy) > 0:
            copy_missing_files(input_folder, files_to_copy, output_folder)

    # Next is the English folder; only missing folders should be copied,
    # missing files should not be copied.
    (folders_to_copy, files_to_copy) = find_missing_entries(english_folder, output_folder)
    if len(folders_to_copy) > 0:
        copy_missing_folders(english_folder, folders_to_copy, output_folder)


def apply_to_every_other_part(content, separator, func, param1):
    """
    Splits the content by the given separator
    and applies the given function to every other part (0th, 2nd, 4th and so on)
    keeping the rest (1st, 3rd, 5th and so on) intact
    """
    parts = content.split(separator)
    processed_parts = []

    for i in range(len(parts)):
        part = parts[i]
        if (i % 2) == 0:
            processed_parts.append(func(part, param1))
        else:
            processed_parts.append(parts[i])

    return separator.join(processed_parts)