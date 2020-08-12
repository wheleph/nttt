from .tidyup import tidyup_translations

def main():
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Nina's Translation Tidyup Tool v 0.1.1-SNAPSHOT")
    parser.add_argument("-i", "--input", help="The input directory which contains the content to tidy up, defaults to the current directory.")
    parser.add_argument("-o", "--output", help="The output directory where the upgraded content should be written, defaults to the same as directory.")
    parser.add_argument("-df", "--dangerous_features", help="True/False, enables some features that could be dangerous, defaults to True.")
    args = parser.parse_args()

    if args.input:
        input_folder = args.input
    else:
        input_folder = "."

    if args.output:
        output_folder = args.output
    else:
        output_folder = input_folder

    if args.dangerous_features:
        dangerous_features = args.dangerous_features
    else:
        dangerous_features = True


    tidyup_translations(input_folder, output_folder, dangerous_features)
