from .arguments import parse_command_line, resolve_arguments, check_arguments, show_arguments
from .tidyup import tidyup_translations

def main():
    command_line_args = parse_command_line()
    resolved_arguments = resolve_arguments(command_line_args)
    show_arguments(resolved_arguments)
    if (check_arguments(resolved_arguments)):
        tidyup_translations(resolved_arguments)
