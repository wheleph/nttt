import unittest
import nttt
import os
from pathlib import Path
from tempfile import TemporaryDirectory

class TestArguments(unittest.TestCase):

    def test_get_final_step(self):
        ''' Test case for the get_final_step function:
        - If there are no step files, the function should return 0.
        - If there is one step file, called step_1.md, the function should return 1.
        - If there are two step files, called step_1.md and step_2.md, the function should return 2.
        - If there are three step files, called step_1.md, step__2.md and step_4.md, the function should return 2.
        '''

        with TemporaryDirectory() as temp_folder:
            result = nttt.arguments.get_final_step(temp_folder)
            self.assertEqual(result, 0)

            step_file = nttt.arguments.get_step_file(temp_folder, 1)
            step_file.touch()
            result = nttt.arguments.get_final_step(temp_folder)
            self.assertEqual(result, 1)

            step_file = nttt.arguments.get_step_file(temp_folder, 2)
            step_file.touch()
            result = nttt.arguments.get_final_step(temp_folder)
            self.assertEqual(result, 2)

            step_file = nttt.arguments.get_step_file(temp_folder, 4)
            step_file.touch()
            result = nttt.arguments.get_final_step(temp_folder)
            self.assertEqual(result, 2)

    def test_get_arguments(self):
        ''' Test case for the get_arguments function:
        - Without any command line arguments specified, the defaults are used.
        - With the command line arguments specified, those values are used.
        '''

        if os.name == 'nt':
            # FIXME: This test case doesn't run on Windows, because the os.chdir function doesn't seem to
            # work on Path objects.
            return

        class CommandLineArgs():
            def __init__(self):
                self.input =      False
                self.output =     False
                self.english =    False
                self.language =   False
                self.volunteers = False
                self.final =      False

        with TemporaryDirectory() as temp_folder:
            input_folder = Path("{}{}hi-IN".format(temp_folder, os.sep))
            english_folder = Path("{}{}en".format(temp_folder, os.sep))
            os.mkdir(input_folder)
            os.chdir(input_folder)

            # Defaults for all arguments.
            command_line_args = CommandLineArgs()
            arguments = nttt.arguments.get_arguments(command_line_args)
            self.assertEqual(arguments[nttt.arguments.Constants.INPUT],      input_folder)
            self.assertEqual(arguments[nttt.arguments.Constants.OUTPUT],     input_folder)
            self.assertEqual(arguments[nttt.arguments.Constants.ENGLISH],    english_folder)
            self.assertEqual(arguments[nttt.arguments.Constants.LANGUAGE],   "hi-IN")
            self.assertEqual(arguments[nttt.arguments.Constants.VOLUNTEERS], [])
            self.assertEqual(arguments[nttt.arguments.Constants.FINAL],      0)

            input_folder = Path("{}{}da-DK".format(temp_folder, os.sep))
            output_folder = Path("{}{}output".format(temp_folder, os.sep))
            english_folder = Path("{}{}en-GB".format(temp_folder, os.sep))
            os.chdir(temp_folder)

            # Specify all arguments.
            command_line_args.input =      "da-DK"
            command_line_args.output =     "output"
            command_line_args.english =    "en-GB"
            command_line_args.language =   "de-DE"
            command_line_args.volunteers = " Volunteer One , Volunteer Two "
            command_line_args.final =      5
            arguments = nttt.arguments.get_arguments(command_line_args)
            self.assertEqual(arguments[nttt.arguments.Constants.INPUT],      input_folder)
            self.assertEqual(arguments[nttt.arguments.Constants.OUTPUT],     output_folder)
            self.assertEqual(arguments[nttt.arguments.Constants.ENGLISH],    english_folder)
            self.assertEqual(arguments[nttt.arguments.Constants.LANGUAGE],   "de-DE")
            self.assertEqual(arguments[nttt.arguments.Constants.VOLUNTEERS], ["Volunteer One", "Volunteer Two"])
            self.assertEqual(arguments[nttt.arguments.Constants.FINAL],      5)

    def test_check_folder(self):
        ''' Test case for the check_folder function:
        - The function should return True for an existing folder.
        - The function should return False for an existing file.
        - The function should return False for non-existing folder.
        '''

        with TemporaryDirectory() as temp_folder:
            result = nttt.arguments.check_folder(temp_folder)
            self.assertEqual(result, True)

            test_file = Path("{}{}test_file".format(temp_folder, os.sep))
            test_file.touch()
            result = nttt.arguments.check_folder(test_file)
            self.assertEqual(result, False)

            test_dir = Path("{}{}test_dir".format(temp_folder, os.sep))
            result = nttt.arguments.check_folder(test_dir)
            self.assertEqual(result, False)

            os.mkdir(test_dir)
            result = nttt.arguments.check_folder(test_dir)
            self.assertEqual(result, True)

    def test_check_step_file(self):
        ''' Test case for the check_step_file function:
        - The function should return False for a non-existing file.
        - The function should return True for an existing file.
        '''

        with TemporaryDirectory() as temp_folder:
            result = nttt.arguments.check_step_file(temp_folder, 3)
            self.assertEqual(result, False)

            step_file = nttt.arguments.get_step_file(temp_folder, 3)
            step_file.touch()
            result = nttt.arguments.check_step_file(temp_folder, 3)
            self.assertEqual(result, True)

    def test_check_arguments(self):
        ''' Test case for the check_arguments function:
        - The function should return False if the input folder doesn't exist.
        - The function should return False if the English folder doesn't exist.
        - The function should return False if the output folder exists, but is not a folder.
        - The function should return False if the final step is specified, but the step file doesn't exist.
        - The function should return True in any other case.
        '''

        with TemporaryDirectory() as temp_folder:
            arguments = {}
            arguments[nttt.arguments.Constants.INPUT] =      Path("{}{}uk-UA".format(temp_folder, os.sep))
            arguments[nttt.arguments.Constants.OUTPUT] =     Path("{}{}output".format(temp_folder, os.sep))
            arguments[nttt.arguments.Constants.ENGLISH] =    Path("{}{}en".format(temp_folder, os.sep))
            arguments[nttt.arguments.Constants.LANGUAGE] =   "uk-UA"
            arguments[nttt.arguments.Constants.VOLUNTEERS] = []
            arguments[nttt.arguments.Constants.FINAL] =      0

            # Input and English folder don't exist. Output folder and final step are OK.
            result = nttt.arguments.check_arguments(arguments)
            self.assertEqual(result, False)

            # Create input folder. English folder still doesn't exist.
            os.mkdir(arguments[nttt.arguments.Constants.INPUT])
            result = nttt.arguments.check_arguments(arguments)
            self.assertEqual(result, False)

            # Create English folder as well.
            os.mkdir(arguments[nttt.arguments.Constants.ENGLISH])
            result = nttt.arguments.check_arguments(arguments)
            self.assertEqual(result, True)

            # Final step file doesn't exist.
            arguments[nttt.arguments.Constants.FINAL] = 3
            result = nttt.arguments.check_arguments(arguments)
            self.assertEqual(result, False)

            # Create final step file.
            step_file = nttt.arguments.get_step_file(arguments[nttt.arguments.Constants.INPUT], 3)
            step_file.touch()
            result = nttt.arguments.check_arguments(arguments)
            self.assertEqual(result, True)

            # Create output folder as file.
            arguments[nttt.arguments.Constants.OUTPUT].touch()
            result = nttt.arguments.check_arguments(arguments)
            self.assertEqual(result, False)

            # Create proper output folder.
            os.remove(arguments[nttt.arguments.Constants.OUTPUT])
            os.mkdir(arguments[nttt.arguments.Constants.OUTPUT])
            result = nttt.arguments.check_arguments(arguments)
            self.assertEqual(result, True)

if __name__ == "__main__":
    unittest.main()