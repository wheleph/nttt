from .constants import Constants
import os
from pathlib import Path

def get_absolute_path(folder):
    '''Returns the absolute path for the given folder. Trailing path separators and double quotes are also removed.'''

    folder = folder.strip().rstrip(os.pathsep).rstrip('"')
    folder = Path(folder).absolute()
    return folder

def get_final_step(folder):
    '''Returns the number of the final step file.'''

    final_step = 0
    step = 1
    step_file = Path("{}{}step_{}.md".format(folder, os.sep, str(step)))
    while os.path.isfile(step_file):
        final_step = step
        step += 1
        step_file = Path("{}{}step_{}.md".format(folder, os.sep, str(step)))
    return final_step

def get_arguments():
    '''Returns the command line arguments. For arguments that are not provided ont he command line, the default if used.'''

    from argparse import ArgumentParser
    from os.path import basename, dirname

    parser = ArgumentParser(description="Nina's Translation Tidyup Tool v 0.1.1-SNAPSHOT")
    parser.add_argument("-i", "--input",      help = "The input directory which contains the content to tidy up, defaults to the current directory.")
    parser.add_argument("-o", "--output",     help = "The output directory where the upgraded content should be written, defaults to the same as INPUT.")
    parser.add_argument("-e", "--english",    help = "The directory which contains the English files and folders, defaults to INPUT/../en.")
    parser.add_argument("-l", "--language",   help = "The language of the content to be tidied up, defaults to basename(INPUT).")
    parser.add_argument("-v", "--volunteers", help = "The list of volunteers as a comma separated list, defaults to an empty list.")
    parser.add_argument("-f", "--final",      help = "The number of the final step file, defaults to the step file with the highest number.")
    args = parser.parse_args()

    arguments = {}

    if args.input:
        arguments[Constants.INPUT] = get_absolute_path(args.input)
    else:
        arguments[Constants.INPUT] = get_absolute_path('.')

    if args.output:
        arguments[Constants.OUTPUT] = get_absolute_path(args.output)
    else:
        arguments[Constants.OUTPUT] = arguments[Constants.INPUT]

    if args.english:
        arguments[Constants.ENGLISH] = get_absolute_path(args.english)
    else:
        arguments[Constants.ENGLISH] = dirname(arguments[Constants.INPUT]) + os.sep + 'en'

    if args.language:
        arguments[Constants.LANGUAGE] = args.language
    else:
        arguments[Constants.LANGUAGE] = basename(arguments[Constants.INPUT])

    if args.volunteers:
        arguments[Constants.VOLUNTEERS] = [name.strip() for name in args.volunteers.split(',')]
    else:
        arguments[Constants.VOLUNTEERS] = []

    if args.final:
        arguments[Constants.FINAL] = int(args.final)
    else:
        arguments[Constants.FINAL] = get_final_step(arguments[Constants.INPUT])

    return arguments

def show_arguments(arguments):
    '''Shows the given arguments.'''

    if arguments[Constants.INPUT] == arguments[Constants.OUTPUT]:
        print("Using folder - {}".format(arguments[Constants.INPUT]))
    else:
        print("Input folder - '{}'".format(arguments[Constants.INPUT]))
        print("Output folder - '{}'".format(arguments[Constants.OUTPUT]))
    print("English folder - '{}'".format(arguments[Constants.ENGLISH]))
    print("Language - '{}'".format(arguments[Constants.LANGUAGE]))
    print("Volunteers - '{}'".format(arguments[Constants.VOLUNTEERS]))
    print("Final step - '{}'".format(arguments[Constants.FINAL]))

def check_folder(folder):
    '''Checks whether the given folder exists and is a directory.'''

    import sys

    valid = True
    if not os.path.isdir(folder):
        valid = False;
        print("Folder '{}' not found".format(folder), file=sys.stderr)
    return valid

def check_arguments(arguments):
    '''Checks whether the given arguments are valid.'''

    valid = True
    if not check_folder(arguments[Constants.INPUT]):
        valid = False;
    if not check_folder(arguments[Constants.ENGLISH]):
        valid = False;
    return valid