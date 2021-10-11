import pandas
import sys
from .utilities import get_file, save_file


# In case of an empty spreadsheet cell, pandas will return a float value NaN.
# In string format, this becomes 'nan'.
EMPTY_CELL_AS_STRING = 'nan'


def get_volunteer_acknowledgement(csv_file_path, language):
    '''
    Returns the volunteer acknowledgement for the given language or None if
    the volunteer acknowledgement doesn't exist.
    '''

    data_frame = None
    try:
        data_frame = pandas.read_csv(csv_file_path)
    except:
        print("Could not read the volunteer acknowledgements spreadsheet.",
              file=sys.stderr)
        return None

    for i in data_frame.index:
        if data_frame.at[i, 'Locale'] == language:
            return data_frame.at[i, 'Acknowledgement']
    return None


def add_volunteer_acknowledgement(csv_file_path, output_file_path, language,
                                  volunteers, logging):
    '''
    Adds the volunteer acknowledgement to the given output file. Returns
    whether the volunteer acknowledgement was successfully added.
    '''

    if logging == "on":
        print("Using the volunteer acknowledgements from {}".format(csv_file_path))

    acknowledgement = get_volunteer_acknowledgement(csv_file_path, language)
    if acknowledgement is None:
        print("Could not find the volunteer acknowledgement for language {}".format(language),
              file=sys.stderr)
        return False
    elif str(acknowledgement) == EMPTY_CELL_AS_STRING:
        print("Empty volunteer acknowledgement for language {}".format(language),
              file=sys.stderr)
        return False

    name_placeholders = "[name]\n\n[name]\n\n[name]\n"
    if name_placeholders not in acknowledgement:
        print("Incorrect volunteer acknowledgement for language {}".format(language),
              file=sys.stderr)
        return False

    content, suggested_eol = get_file(output_file_path)
    if "***\n" in content:
        print("Volunteer acknowledgement already present in file {}".format(output_file_path),
              file=sys.stderr)
        return False

    if len(volunteers) == 0:
        print("Warning: No volunteer name(s) given - please add them manually")
    else:
        volunteer_names = '\n'.join(volunteers) + '\n'
        acknowledgement = acknowledgement.replace(name_placeholders,
                                                  volunteer_names)
    if logging == "on":
        print("Volunteer acknowledgement to be added:")
        print(acknowledgement)

    # Strip trailings blanks (spaces, tabs, newlines) from the original content
    # before appending the volunteer acknowledgement. This avoids a surplus of
    # empty lines between the content and the volunteer acknowledgement.
    content = content.rstrip() + "\n\n***\n" + acknowledgement + "\n"
    save_file(output_file_path, content, suggested_eol)
    return True
