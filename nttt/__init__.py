from .arguments import get_arguments, check_arguments, show_arguments
from .tidyup import tidyup_translations

def main():
    arguments = get_arguments()
    show_arguments(arguments)
    if (check_arguments(arguments)):
        tidyup_translations(arguments)