import pandas
from .utilities import get_file, save_file


def get_volunteer_acknowledgement(csv_file_path, language):
    '''
    Returns the volunteer acknowledgement for the given language or None if
    the volunteer acknowledgement doesn't exist.
    '''

    data_frame = None
    try:
        data_frame = pandas.read_csv(csv_file_path)
    except:
        print("ERROR: Could not read the volunteer acknowledgements spreadsheet.")
        return None

    acknowledgement = None
    for i in data_frame.index:
        if data_frame.at[i, 'Locale'] == language:
            acknowledgement = data_frame.at[i, 'Acknowledgement']
            break
    return acknowledgement


def add_volunteer_acknowledgement(csv_file_path, output_file_path, language,
                                  volunteers, logging):
    '''
    Adds the volunteer acknowledgement to the given output file. Returns
    whether the volunteer acknowledgement was successfully added.
    '''

    acknowledgement = get_volunteer_acknowledgement(csv_file_path, language)
    if acknowledgement is None:
        print("ERROR: Could not find the volunteer acknowledgement for language {}".format(language))
        return False

    if len(volunteers) == 0:
        print("WARNING: No volunteer name(s) given - please add them manually")
    else:
        volunteer_names = ""
        first = True
        for volunteer in volunteers:
            if first:
                first = False
                volunteer_names = volunteer + "\n"
            else:
                volunteer_names = volunteer_names + "\n" + volunteer + "\n"
        acknowledgement = acknowledgement.replace("[name]\n\n[name]\n\n[name]\n", volunteer_names)
    if logging == "on":
        print("Volunteer acknowledgement to be added:")
        print(acknowledgement)

    content, suggested_eol = get_file(output_file_path)
    # Strip trailings blanks (spaces, tabs, newlines) from the original content
    # before appending the volunteer acknowledgement. This avoids a surplus of
    # empty lines between the content and the volunteer acknowledgement.
    content = content.rstrip() + "\n\n" + acknowledgement + "\n"
    save_file(output_file_path, content, suggested_eol)
    return True
