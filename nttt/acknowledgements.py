import pandas
from .utilities import get_file, save_file

def add_volunteer_acknowledgement(csv_file_path, output_file_path, language, volunteers, logging):
    '''Adds the volunteer acknowledgement to the given output file.'''

    data_frame = None
    try:
        data_frame = pandas.read_csv(csv_file_path)
    except:
        print("ERROR: Could not read the volunteer acknowledgements spreadsheet.")
        return

    acknowledgement = None
    for i in data_frame.index:
        if data_frame.at[i, 'Locale'] == language:
            acknowledgement = data_frame.at[i, 'Acknowledgement']
            break
    if acknowledgement is None:
        print("ERROR: Could not find the volunteer acknowledgement for language {}".format(language))
        return

    if len(volunteers) == 0:
        print("No volunteer name(s) given - please add them manually")
    else:
        volunteer_names = ""
        first = True
        for volunteer in volunteers:
            if first:
                first = False
                volunteer_names = volunteer + "\n"
            else:
                volunteer_names = volunteer_names + "\n" + volunteer + "\n"
        acknowledgement.replace("[name]\n\n[name]\n\n[name]\n", volunteer_names)
    if logging == "on":
        print("Volunteer acknowledgement to be added:")
        print(acknowledgement)

    content, suggested_eol = get_file(output_file_path)
    content = content + "\n|" + acknowledgement + "\n"
    save_file(output_file_path, content, suggested_eol)
