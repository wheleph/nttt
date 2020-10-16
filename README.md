# NTTT

"Nina's Translation Tidy-up Tool"

Note - NTTT will work on Windows, macOS and Linux.

## Install

To install NTTT, clone the repository and use `pip3` to install:

```bash
git clone https://github.com/wheleph/nttt
cd nttt
pip3 install -r requirements.txt
pip3 install . --upgrade
```

![install nttt](images/install_nttt.png)

You can uninstall nttt using:

```bash
pip3 uninstall nttt
```

## Usage

NTTT is a command line tool, called using `nttt`.

Navigate to the directory you want to tidy up and run NTTT:

```bash
cd path\to\project\de-DE
nttt
```

NTTT will search for all relevant files and ask you to confirm before updating.

![run nttt](images/run_nttt.png)


### Input and output directories

You can specify different directories for the input and output folder using the `-i`/`--input` and `-o`/`--output` options:

```bash
nttt --input c:\path\to\project\de-DE --output c:\path\to\project\de-DE-tidy
```

### Help

To bring up full usage information use the `-h`/`--help` option.

```bash
nttt -h

usage: nttt [-h] [-i INPUT] [-o OUTPUT] [-e ENGLISH] [-l LANGUAGE] [-v VOLUNTEERS] [-f FINAL]

Nina's Translation Tidyup Tool

optional arguments:
  -h, --help            Show this help message and exit.
  -i INPUT, --input INPUT
                        The input directory which contains the content to tidy
                        up, defaults to the current folder.
  -o OUTPUT, --output OUTPUT
                        The output directory where the upgraded content should
                        be written, defaults to the same as input.
  -e ENGLISH, --english ENGLISH
                        The directory which contains the English files and
                        folders, defaults to INPUT/../en.
  -l LANGUAGE, --language LANGUAGE
                        The language of the content to be tidied up, defaults
                        to basename(INPUT).
  -v VOLUNTEERS, --volunteers VOLUNTEERS
                        The list of volunteers as a comma separated list,
                        defaults to an empty list.
  -f FINAL, --final FINAL
                        The number of the final step file, defaults to the
                        step file with the highest number.

examples of usage:
  nttt
    Use the current directory (.) as input and output directory, ../en
    (..\en on Windows) as English directory, and the last part of the
    full path to the current directory as language. No volunteer names
    will be added to the final step file and the step file with the
    highest number is used as final step file.

  nttt -i path/to/project/de-DE (macOS and Linux)
  nttt -i path\to\project\de-DE (Windows)
    Use path/to/project/de-DE (path\to\project\de-DE on Windows) as input
    and output directory, path/to/project/en as English directory and de-DE
    as language. No volunteer names will be added to the final step file
    and the step file with the highest number is used as final step file.

  nttt -o ../output (macOS and Linux)
  nttt -o ..\output (Windows)
    Use the current directory (.) as input directory, ../output
    (..\output on Windows) as output directory, ../en
    (..\en on Windows) as English directory, and the last part of the
    full path to the current directory as language. No volunteer names
    will be added to the final step file and the step file with the
    highest number is used as final step file.

  nttt -e some/other/path/en (macOS and Linux)
  nttt -e some\other\path\en (Windows)
    Use the current directory (.) as input and output directory,
    some/other/path/en (some\other\path\en on Windows) as English
    directory, and the last part of the full path to the current
    directory as language. No volunteer names will be added to the
    final step file and the step file with the highest number is
    used as final step file.

  nttt -l hi-IN
    Use path/to/project/de-DE (path\to\project\de-DE on Windows) as input
    and output directory, path/to/project/en as English directory and hi-IN
    as language. No volunteer names will be added to the final step file
    and the step file with the highest number is used as final step file.

  nttt -v "Volunteer Translator, Volunteer Reviewer, Volunteer Tester"
    Use the current directory (.) as input and output directory, ../en
    (..\en on Windows) as English directory, and the last part of the
    full path to the current directory as language. Three volunteer names
    are added to the final step file: "Volunteer Translator",
    "Volunteer Reviewer" and "Volunteer Tester". The step file with the
    highest number is used as final step file.
    Note that the list of volunteer names should be enclosed in quotes.
    Also note that spaces at the beginning and end of the list as well
    as spaces before and after commas will be discarded.

  nttt -f 7
    Use the current directory (.) as input and output directory, ../en
    (..\en on Windows) as English directory, and the last part of the
    full path to the current directory as language. No volunteer names
    will be added to the final step file. File step_7.md will be used as
    final step file.

  nttt -i path/to/project/de-DE -o ../output -e some/other/path/en -l hi-IN \
       -v "Volunteer Translator, Volunteer Reviewer, Volunteer Tester" -f 7
    Use path/to/project/de-DE as input directory, ../output as output
    directory, some/other/path/en as English directory, and hi-IN as
    language. Three volunteer names are added to the final step file:
    "Volunteer Translator", "Volunteer Reviewer" and "Volunteer Tester".
    File step_7.md will be used as final step file.
```
