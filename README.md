# NTTT

"Nina's Translation Tidy-up Tool"

Note - NTTT will work on Windows, macOS and Linux.

## Install

To install NTTT, clone the repository and use `pip3` to install:

```bash
git clone https://github.com/raspberrypilearning/nttt
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
```
