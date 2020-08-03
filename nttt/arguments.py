from .constants import INPUT, OUTPUT, ENGLISH, LANGUAGE, VOLUNTEERS, FINAL
import os

def get_arguments():
    from argparse import ArgumentParser
    from os.path import basename, dirname
    from pathlib import Path

    parser = ArgumentParser(description="Nina's Translation Tidyup Tool v 0.1.1-SNAPSHOT")
    parser.add_argument("-i", "--input",      help="The input directory which contains the content to tidy up, defaults to the current directory.")
    parser.add_argument("-o", "--output",     help="The output directory where the upgraded content should be written, defaults to the same as INPUT.")
    parser.add_argument("-e", "--english",    help="The directory which contains the English files and folders, defaults to INPUT/../en.")
    parser.add_argument("-l", "--language",   help="The language of the content to be tidied up, defaults to basename(INPUT).")
    parser.add_argument("-v", "--volunteers", help="The list of volunteers as a comma separated list, defaults to an empty list.")
    parser.add_argument("-f", "--final",      help="The number of the final step file, defaults to the step file with the highest number.")
    args = parser.parse_args()

    arguments = {}

    if args.input:
        arguments[INPUT] = args.input
    else:
        arguments[INPUT] = "."

    if args.output:
        arguments[OUTPUT] = args.output
    else:
        arguments[OUTPUT] = arguments[INPUT]

    if args.english:
        arguments[ENGLISH] = args.english
    else:
        arguments[ENGLISH] = dirname(Path(arguments[INPUT]).absolute()) + os.sep + 'en'

    if args.language:
        arguments[LANGUAGE] = args.language
    else:
        arguments[LANGUAGE] = basename(Path(arguments[INPUT]).absolute())

    if args.volunteers:
        arguments[VOLUNTEERS] = [name.strip() for name in args.volunteers.split(',')]
    else:
        arguments[VOLUNTEERS] = []

    if args.final:
        arguments[FINAL] = int(args.final)
    else:
        # TODO: find step file with highest number
        arguments[FINAL] = -1

    return arguments
