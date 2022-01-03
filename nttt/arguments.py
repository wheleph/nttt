from .constants import ArgumentKeyConstants
import os
from pathlib import Path
from argparse import ArgumentParser


def get_absolute_path(folder):
    '''
    Returns the absolute path for the given folder. Trailing path separators
    and double quotes are also removed.
    '''

    folder = folder.strip().rstrip(os.pathsep).rstrip('"')
    folder = Path(folder).absolute()
    return folder


def get_step_file(folder, step):
    '''Returns the step file for the given step number.'''

    return Path(folder, "step_" + str(step) + ".md")


def get_final_step(folder):
    '''
    Returns the number of the final step file, or 0 in case there are no step
    files.
    '''

    final_step = 0
    step = 1
    step_file = get_step_file(folder, step)
    while os.path.isfile(step_file):
        final_step = step
        step += 1
        step_file = get_step_file(folder, step)
    return final_step


def parse_command_line(version):
    """
    Parses the command line and returns the arguments provided on command line.
    The convention is to begin functional flag names with a small letter
    and non-functional flag names with a capital letter
    """

    parser = ArgumentParser(description="Nina's Translation Tidyup Tool v{}".format(version))
    parser.add_argument("-i", "--input",      help="The input directory which contains the content to tidy up, defaults to the current directory.")
    parser.add_argument("-o", "--output",     help="The output directory where the upgraded content should be written, defaults to the same as INPUT.")
    parser.add_argument("-e", "--english",    help="The directory which contains the English files and folders, defaults to INPUT/../en.")
    parser.add_argument("-l", "--language",   help="The language of the content to be tidied up, defaults to basename(INPUT).")
    parser.add_argument("-v", "--volunteers", help="The list of volunteers as a comma separated list, defaults to an empty list.")
    parser.add_argument("-f", "--final",      help="The number of the final step file, defaults to the step file with the highest number.")
    parser.add_argument("-D", "--Disable",    help="The risky features to be disabled, separated by commas. "
                                                   "Options are: fix_md (fix common markdown-related issues), "
                                                   "fix_html (fix common issues in HTML-like tags (<kbd>Return</kbd>)), "
                                                   "fix_sections (fix common issues in section tags (--- hint ---)), "
                                                   "revert_section_translation (revert translation for section tags), "
                                                   "fix_formatting (fix common issues in formatting tags ({:class=\"block3motion\"})). "
                                                   "Defaults to all risky features to be enabled.")
    parser.add_argument("-L", "--Logging",    help="Logging of modifications. Options are on and off. Default is off.")
    parser.add_argument("-Y", "--Yes",        help="Automatic yes to prompts. "
                                                   "If enabled assume 'yes' as answer to all prompts and run non-interactively. "
                                                   "Options are on and off. Default is off.")
    return parser.parse_args()


def resolve_arguments(command_line_args):
    '''
    Returns the complete set of arguments. For arguments that are not provided
    on the command line, the default is used.
    '''

    from os.path import basename, dirname

    arguments = {}

    if command_line_args.input:
        arguments[ArgumentKeyConstants.INPUT] = get_absolute_path(command_line_args.input)
    else:
        arguments[ArgumentKeyConstants.INPUT] = get_absolute_path('.')

    if command_line_args.output:
        arguments[ArgumentKeyConstants.OUTPUT] = get_absolute_path(command_line_args.output)
    else:
        arguments[ArgumentKeyConstants.OUTPUT] = arguments[ArgumentKeyConstants.INPUT]

    if command_line_args.english:
        arguments[ArgumentKeyConstants.ENGLISH] = get_absolute_path(command_line_args.english)
    else:
        arguments[ArgumentKeyConstants.ENGLISH] = Path(dirname(arguments[ArgumentKeyConstants.INPUT]), 'en')

    if command_line_args.language:
        arguments[ArgumentKeyConstants.LANGUAGE] = command_line_args.language
    else:
        arguments[ArgumentKeyConstants.LANGUAGE] = basename(arguments[ArgumentKeyConstants.INPUT])

    if command_line_args.volunteers:
        arguments[ArgumentKeyConstants.VOLUNTEERS] = [name.strip() for name in command_line_args.volunteers.split(',')]
    else:
        arguments[ArgumentKeyConstants.VOLUNTEERS] = []

    if command_line_args.final:
        arguments[ArgumentKeyConstants.FINAL] = int(command_line_args.final)
    else:
        arguments[ArgumentKeyConstants.FINAL] = get_final_step(arguments[ArgumentKeyConstants.INPUT])

    if command_line_args.Disable:
        arguments[ArgumentKeyConstants.DISABLE] = command_line_args.Disable.split(",")
    else:
        arguments[ArgumentKeyConstants.DISABLE] = []

    if command_line_args.Logging:
        arguments[ArgumentKeyConstants.LOGGING] = command_line_args.Logging
    else:
        arguments[ArgumentKeyConstants.LOGGING] = "off"

    if command_line_args.Yes:
        arguments[ArgumentKeyConstants.YES] = command_line_args.Yes
    else:
        arguments[ArgumentKeyConstants.YES] = "off"

    return arguments


def show_arguments(arguments):
    '''Shows the given arguments.'''

    if arguments[ArgumentKeyConstants.INPUT] == arguments[ArgumentKeyConstants.OUTPUT]:
        print("Using folder - {}".format(arguments[ArgumentKeyConstants.INPUT]))
    else:
        print("Input folder - '{}'".format(arguments[ArgumentKeyConstants.INPUT]))
        print("Output folder - '{}'".format(arguments[ArgumentKeyConstants.OUTPUT]))
    print("English folder - '{}'".format(arguments[ArgumentKeyConstants.ENGLISH]))
    print("Language - '{}'".format(arguments[ArgumentKeyConstants.LANGUAGE]))
    print("Volunteers - '{}'".format(arguments[ArgumentKeyConstants.VOLUNTEERS]))
    print("Final step - '{}'".format(arguments[ArgumentKeyConstants.FINAL]))
    print("Disabled functions - '{}'".format(arguments[ArgumentKeyConstants.DISABLE]))
    print("Logging - '{}'".format(arguments[ArgumentKeyConstants.LOGGING]))
    print("Yes - '{}'".format(arguments[ArgumentKeyConstants.YES]))


def check_folder(folder):
    '''Checks whether the given folder exists and is a directory.'''

    import sys

    valid = True
    if not os.path.isdir(folder):
        valid = False
        print("Folder '{}' not found".format(folder), file=sys.stderr)
    return valid


def check_step_file(folder, step):
    '''Checks whether the step file for the given number exists.'''

    import sys

    valid = True
    step_file = get_step_file(folder, step)
    if not os.path.isfile(step_file):
        valid = False
        print('Step file {} not found.'.format(step_file), file=sys.stderr)
    return valid


def check_arguments(arguments):
    '''Checks whether the given arguments are valid.'''

    valid = True
    if not check_folder(arguments[ArgumentKeyConstants.INPUT]):
        valid = False
    if not check_folder(arguments[ArgumentKeyConstants.ENGLISH]):
        valid = False
    if os.path.exists(arguments[ArgumentKeyConstants.OUTPUT]) and not check_folder(arguments[ArgumentKeyConstants.OUTPUT]):
        valid = False
    if arguments[ArgumentKeyConstants.FINAL] > 0 and not check_step_file(arguments[ArgumentKeyConstants.INPUT], arguments[ArgumentKeyConstants.FINAL]):
        valid = False
    return valid
