import unittest
import nttt
import os
from pathlib import Path
from tempfile import TemporaryDirectory


class TestArguments(unittest.TestCase):

    def test_get_step_file(self):
        '''Test case for the get_step_file function.'''

        with TemporaryDirectory() as temp_folder:
            result = nttt.arguments.get_step_file(temp_folder, 17)
            self.assertEqual(result, Path(str(temp_folder), "step_17.md"))

    def test_get_final_step(self):
        ''' Test case for the get_final_step function:
        - If there are no step files, the function should return 0.
        - If there is one step file, called step_1.md, the function should
          return 1.
        - If there are two step files, called step_1.md and step_2.md, the
          function should return 2.
        - If there are three step files, called step_1.md, step__2.md and
          step_4.md, the function should return 2.
        '''

        with TemporaryDirectory() as temp_folder:
            result = nttt.arguments.get_final_step(temp_folder)
            self.assertEqual(result, 0)

            Path(temp_folder, "step_1.md").touch()
            result = nttt.arguments.get_final_step(temp_folder)
            self.assertEqual(result, 1)

            Path(temp_folder, "step_2.md").touch()
            result = nttt.arguments.get_final_step(temp_folder)
            self.assertEqual(result, 2)

            Path(temp_folder, "step_4.md").touch()
            result = nttt.arguments.get_final_step(temp_folder)
            self.assertEqual(result, 2)

    def test_get_arguments(self):
        ''' Test case for the resolve_arguments function:
        - Without any command line arguments specified, the defaults are used.
        - With the command line arguments specified, those values are used.
        '''

        class CommandLineArgs():
            '''Simple placeholder for command line arguments.'''
            def __init__(self):
                self.input = False
                self.output = False
                self.english = False
                self.language = False
                self.volunteers = False
                self.final = False
                self.Disable = False
                self.Logging = False
                self.Yes = False

        # Using the os.chdir function for a subdirectory of a directory created
        # with TemporaryDirectory doesn't work on Windows and macOS. Therefore,
        # this test case uses directories below the directory that contains
        # this test case (i.e. "unit_test"). These directories have to be
        # present in the repository.
        data_folder = Path(os.getcwd(), "unit_test", "data")
        self.assertTrue(data_folder.is_dir(), "Subdirectory data of directory unit_test is missing.")
        input_folder = Path(data_folder, "hi-IN")
        self.assertTrue(input_folder.is_dir(), "Subdirectory hi-IN of directory data is missing.")
        output_folder = input_folder
        english_folder = Path(data_folder, "en")
        os.chdir(input_folder)

        # Defaults for all arguments.
        command_line_args = CommandLineArgs()
        arguments = nttt.arguments.resolve_arguments(command_line_args)
        self.assertEqual(arguments[nttt.arguments.ArgumentKeyConstants.INPUT], input_folder)
        self.assertEqual(arguments[nttt.arguments.ArgumentKeyConstants.OUTPUT], output_folder)
        self.assertEqual(arguments[nttt.arguments.ArgumentKeyConstants.ENGLISH], english_folder)
        self.assertEqual(arguments[nttt.arguments.ArgumentKeyConstants.LANGUAGE], "hi-IN")
        self.assertEqual(arguments[nttt.arguments.ArgumentKeyConstants.VOLUNTEERS], [])
        self.assertEqual(arguments[nttt.arguments.ArgumentKeyConstants.FINAL], 0)
        self.assertEqual(arguments[nttt.arguments.ArgumentKeyConstants.DISABLE], [])
        self.assertEqual(arguments[nttt.arguments.ArgumentKeyConstants.LOGGING], "off")
        self.assertEqual(arguments[nttt.arguments.ArgumentKeyConstants.YES], "off")

        input_folder = Path(data_folder, "da-DK")
        output_folder = Path(data_folder, "output")
        english_folder = Path(data_folder, "en-GB")
        os.chdir(data_folder)

        # Specify all arguments.
        command_line_args.input = "da-DK"
        command_line_args.output = "output"
        command_line_args.english = "en-GB"
        command_line_args.language = "de-DE"
        command_line_args.volunteers = " Volunteer One , Volunteer Two "
        command_line_args.final = 5
        command_line_args.Disable = "fix_md,fix_html"
        command_line_args.Logging = "on"
        command_line_args.Yes = "on"
        arguments = nttt.arguments.resolve_arguments(command_line_args)
        self.assertEqual(arguments[nttt.arguments.ArgumentKeyConstants.INPUT], input_folder)
        self.assertEqual(arguments[nttt.arguments.ArgumentKeyConstants.OUTPUT], output_folder)
        self.assertEqual(arguments[nttt.arguments.ArgumentKeyConstants.ENGLISH], english_folder)
        self.assertEqual(arguments[nttt.arguments.ArgumentKeyConstants.LANGUAGE], "de-DE")
        self.assertEqual(arguments[nttt.arguments.ArgumentKeyConstants.VOLUNTEERS], ["Volunteer One", "Volunteer Two"])
        self.assertEqual(arguments[nttt.arguments.ArgumentKeyConstants.FINAL], 5)
        self.assertEqual(arguments[nttt.arguments.ArgumentKeyConstants.DISABLE], ["fix_md", "fix_html"])
        self.assertEqual(arguments[nttt.arguments.ArgumentKeyConstants.LOGGING], "on")
        self.assertEqual(arguments[nttt.arguments.ArgumentKeyConstants.YES], "on")

    def test_check_folder(self):
        ''' Test case for the check_folder function:
        - The function should return True for an existing folder.
        - The function should return False for an existing file.
        - The function should return False for non-existing folder.
        '''

        with TemporaryDirectory() as temp_folder:
            result = nttt.arguments.check_folder(temp_folder)
            self.assertTrue(result)

            test_file = Path(temp_folder, "test_file")
            test_file.touch()
            result = nttt.arguments.check_folder(test_file)
            self.assertFalse(result)

            test_dir = Path(temp_folder, "test_dir")
            result = nttt.arguments.check_folder(test_dir)
            self.assertFalse(result)

            os.mkdir(test_dir)
            result = nttt.arguments.check_folder(test_dir)
            self.assertTrue(result)

    def test_check_step_file(self):
        ''' Test case for the check_step_file function:
        - The function should return False for a non-existing file.
        - The function should return True for an existing file.
        '''

        with TemporaryDirectory() as temp_folder:
            result = nttt.arguments.check_step_file(temp_folder, 3)
            self.assertFalse(result)

            Path(temp_folder, "step_3.md").touch()
            result = nttt.arguments.check_step_file(temp_folder, 3)
            self.assertTrue(result)

    def test_check_arguments(self):
        ''' Test case for the check_arguments function:
        - The function should return False if the input folder doesn't exist.
        - The function should return False if the English folder doesn't exist.
        - The function should return False if the output folder exists, but is
          not a folder.
        - The function should return False if the final step is specified, but
          the step file doesn't exist.
        - The function should return True in any other case.
        '''

        with TemporaryDirectory() as temp_folder:
            arguments = {}
            arguments[nttt.arguments.ArgumentKeyConstants.INPUT] = Path(temp_folder, "uk-UA")
            arguments[nttt.arguments.ArgumentKeyConstants.OUTPUT] = Path(temp_folder, "output")
            arguments[nttt.arguments.ArgumentKeyConstants.ENGLISH] = Path(temp_folder, "en")
            arguments[nttt.arguments.ArgumentKeyConstants.LANGUAGE] = "uk-UA"
            arguments[nttt.arguments.ArgumentKeyConstants.VOLUNTEERS] = []
            arguments[nttt.arguments.ArgumentKeyConstants.FINAL] = 0

            # Input and English folder don't exist. Output folder and final step are OK.
            result = nttt.arguments.check_arguments(arguments)
            self.assertFalse(result)

            # Create input folder. English folder still doesn't exist.
            os.mkdir(arguments[nttt.arguments.ArgumentKeyConstants.INPUT])
            result = nttt.arguments.check_arguments(arguments)
            self.assertFalse(result)

            # Create English folder as well.
            os.mkdir(arguments[nttt.arguments.ArgumentKeyConstants.ENGLISH])
            result = nttt.arguments.check_arguments(arguments)
            self.assertTrue(result)

            # Final step file doesn't exist.
            arguments[nttt.arguments.ArgumentKeyConstants.FINAL] = 3
            result = nttt.arguments.check_arguments(arguments)
            self.assertFalse(result)

            # Create final step file.
            Path(arguments[nttt.arguments.ArgumentKeyConstants.INPUT], "step_3.md").touch()
            result = nttt.arguments.check_arguments(arguments)
            self.assertTrue(result)

            # Create output folder as file.
            arguments[nttt.arguments.ArgumentKeyConstants.OUTPUT].touch()
            result = nttt.arguments.check_arguments(arguments)
            self.assertFalse(result)

            # Create proper output folder.
            os.remove(arguments[nttt.arguments.ArgumentKeyConstants.OUTPUT])
            os.mkdir(arguments[nttt.arguments.ArgumentKeyConstants.OUTPUT])
            result = nttt.arguments.check_arguments(arguments)
            self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
