from .tidyup import tidyup_translations

def main():
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Nina's Translation Tidyup Tool v 0.1.0")
    parser.add_argument("-i", "--input", help="The input directory which contains the content to tidy up, defaults to the current directory.")
    parser.add_argument("-o", "--output", help="The output directory where the upgraded content should be written, defaults to the same as directory.")
    args = parser.parse_args()
    
    if args.input:
        input_folder = args.input
    else:
        input_folder = "."

    if args.output:
        output_folder = args.output
    else:
        output_folder = input_folder
    tidyup_translations(input_folder, output_folder)
