from .arguments import parse_command_line, get_arguments, check_arguments, show_arguments
from .tidyup import tidyup_translations

def main():
    command_line_args = parse_command_line()
    arguments = get_arguments(command_line_args)
    show_arguments(arguments)
    if (check_arguments(arguments)):
        tidyup_translations(arguments)