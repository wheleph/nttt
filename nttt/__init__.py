from .arguments import get_arguments
from .tidyup import tidyup_translations

def main():
    tidyup_translations(get_arguments())
