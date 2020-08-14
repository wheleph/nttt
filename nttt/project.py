import os
from pathlib import Path
import shutil


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

    print("Copying folders from {} to {}:".format(source_folder, dest_folder))
    for folder_to_copy in folders_to_copy:
        print(" - {}".format(folder_to_copy))

    for folder_to_copy in folders_to_copy:
        source_path = Path(source_folder, folder_to_copy)
        dest_path = Path(dest_folder, folder_to_copy)
        shutil.copytree(source_path, dest_path)


def copy_missing_files(source_folder, files_to_copy, dest_folder):
    '''
    Copies the given files from the source folder to the destination folder.
    '''

    print("Copying files from {} to {}:".format(source_folder, dest_folder))
    for file_to_copy in files_to_copy:
        print(" - {}".format(file_to_copy))

    for file_to_copy in files_to_copy:
        source_path = Path(source_folder, file_to_copy)
        dest_path = Path(dest_folder, file_to_copy)
        shutil.copyfile(source_path, dest_path)


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
