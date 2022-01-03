class GeneralConstants:
    FILE_NAME_META_YML = "meta.yml"
    VOLUNTEER_ACKNOWLEDGEMENTS_CSV = (
        "https://docs.google.com/spreadsheets/d/e/"
        "2PACX-1vS_oJDVBL9f0YQxISmtcCp8V1Hf4zjw1BwIhm-w5GMsvA8Y4VdT9JAUSueRXI5me5usLjblEPsNlqIH/"
        "pub?gid=1717165158&single=true&output=csv")


class ArgumentKeyConstants:
    # Keys for the arguments dictionary
    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'
    ENGLISH = 'ENGLISH'
    LANGUAGE = 'LANGUAGE'
    VOLUNTEERS = 'VOLUNTEERS'
    FINAL = 'FINAL'
    DISABLE = 'DISABLE'
    LOGGING = 'LOGGING'
    YES = 'YES'


class RegexConstants:
    # Matches various spaces (but no newlines). The list is taken from http://jkorpela.fi/chars/spaces.html
    SPACES = " \t\u00A0\u1680\u180E\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200A\u200B" \
                  "\u202F\u205F\u3000\uFEFF"
    COLONS = ":："
    QUOTES = '"”“«»'
