import unittest
import nttt
import os
from pathlib import Path
from tempfile import TemporaryDirectory


class TestAcknowledgements(unittest.TestCase):

    FIRST_LINE = "Dit project werd vertaald door vrijwilligers:"
    LAST_LINE = ("Dankzij vrijwilligers kunnen we mensen over de hele wereld "
                 "de kans geven om in hun eigen taal te leren. Jij kunt ons "
                 "helpen meer mensen te bereiken door vrijwillig te starten "
                 "met vertalen - meer informatie op "
                 "[rpf.io/translate](https://rpf.io/translate).")

    def test_missing_csv_file(self):
        '''
        Test case for the situation where the CSV file is missing (or not
        accessible).
        '''

        with TemporaryDirectory() as temp_folder:
            csv_file_path = Path(temp_folder, "volunteer_acknowledgements.csv")
            language = "nl-NL"
            result = nttt.acknowledgements.get_volunteer_acknowledgement(
                csv_file_path, language)
            self.assertIsNone(result)

    def test_missing_language(self):
        '''
        Test case for the situation where the requested language is not present
        in the CSV file.
        '''

        with TemporaryDirectory() as temp_folder:
            data_folder = Path(os.getcwd(), "unit_test", "data")
            self.assertTrue(
                data_folder.is_dir(),
                "Subdirectory data of directory unit_test is missing.")
            csv_file_path = Path(data_folder, "volunteer_acknowledgements.csv")
            language = "nl-BE"
            result = nttt.acknowledgements.get_volunteer_acknowledgement(
                csv_file_path, language)
            self.assertIsNone(result)

            output_file_path = Path(temp_folder, "final_step.md")
            output_file_path.touch()
            volunteers = []
            logging = "off"
            result = nttt.acknowledgements.add_volunteer_acknowledgement(
                csv_file_path, output_file_path, language, volunteers, logging)
            self.assertFalse(result)

    def test_missing_acknowledgement(self):
        '''
        Test case for the situation where the acknowledgement for the requested
        language in the CSV file is empty.
        '''

        with TemporaryDirectory() as temp_folder:
            data_folder = Path(os.getcwd(), "unit_test", "data")
            self.assertTrue(
                data_folder.is_dir(),
                "Subdirectory data of directory unit_test is missing.")
            csv_file_path = Path(data_folder, "volunteer_acknowledgements.csv")
            output_file_path = Path(temp_folder, "final_step.md")
            output_file_path.touch()
            language = "et-EE"
            volunteers = []
            logging = "off"
            result = nttt.acknowledgements.add_volunteer_acknowledgement(
                csv_file_path, output_file_path, language, volunteers, logging)
            self.assertFalse(result)

    def test_incorrect_acknowledgement(self):
        '''
        Test case for the situation where the acknowledgement for the requested
        language in the CSV file is incorrect, i.e. doesn't have three name
        placeholders with empty lines in between.
        '''

        with TemporaryDirectory() as temp_folder:
            data_folder = Path(os.getcwd(), "unit_test", "data")
            self.assertTrue(
                data_folder.is_dir(),
                "Subdirectory data of directory unit_test is missing.")
            csv_file_path = Path(data_folder, "volunteer_acknowledgements.csv")
            output_file_path = Path(temp_folder, "final_step.md")
            output_file_path.touch()
            language = "fil-PH"
            volunteers = []
            logging = "off"
            result = nttt.acknowledgements.add_volunteer_acknowledgement(
                csv_file_path, output_file_path, language, volunteers, logging)
            self.assertFalse(result)

    def test_no_volunteer_names(self):
        '''
        Test case for the situation where the list of volunteer names is empty.
        '''

        with TemporaryDirectory() as temp_folder:
            data_folder = Path(os.getcwd(), "unit_test", "data")
            self.assertTrue(
                data_folder.is_dir(),
                "Subdirectory data of directory unit_test is missing.")
            csv_file_path = Path(data_folder, "volunteer_acknowledgements.csv")
            output_file_path = Path(temp_folder, "final_step.md")
            output_file_path.touch()
            language = "nl-NL"
            volunteers = []
            logging = "off"
            result = nttt.acknowledgements.add_volunteer_acknowledgement(
                csv_file_path, output_file_path, language, volunteers, logging)
            self.assertTrue(result)

            # Check contents of final_step.md.
            contents = output_file_path.read_text()
            expected_contents = '\n'.join(["",
                                           "***",
                                           self.FIRST_LINE,
                                           "",
                                           "[name]",
                                           "",
                                           "[name]",
                                           "",
                                           "[name]",
                                           "",
                                           self.LAST_LINE,
                                           ""])
            self.assertEqual(contents, expected_contents)

    def test_one_volunteer_name(self):
        '''
        Test case for the situation where there is one volunteer name.
        '''

        with TemporaryDirectory() as temp_folder:
            data_folder = Path(os.getcwd(), "unit_test", "data")
            self.assertTrue(
                data_folder.is_dir(),
                "Subdirectory data of directory unit_test is missing.")
            csv_file_path = Path(data_folder, "volunteer_acknowledgements.csv")
            output_file_path = Path(temp_folder, "final_step.md")
            output_file_path.touch()
            language = "nl-NL"
            volunteers = ["Volunteer One"]
            logging = "off"
            result = nttt.acknowledgements.add_volunteer_acknowledgement(
                csv_file_path, output_file_path, language, volunteers, logging)
            self.assertTrue(result)

            # Check contents of final_step.md.
            contents = output_file_path.read_text()
            expected_contents = '\n'.join(["",
                                           "***",
                                           self.FIRST_LINE,
                                           "",
                                           "Volunteer One",
                                           "",
                                           self.LAST_LINE,
                                           ""])
            self.assertEqual(contents, expected_contents)

    def test_four_volunteer_names(self):
        '''
        Test case for the situation where there are four volunteer names.
        '''

        with TemporaryDirectory() as temp_folder:
            data_folder = Path(os.getcwd(), "unit_test", "data")
            self.assertTrue(
                data_folder.is_dir(),
                "Subdirectory data of directory unit_test is missing.")
            csv_file_path = Path(data_folder, "volunteer_acknowledgements.csv")
            output_file_path = Path(temp_folder, "final_step.md")
            output_file_path.touch()
            language = "nl-NL"
            volunteers = ["Volunteer One", "Vrijwilliger Twee",
                          "Freiwillige Drei", "Voluntario Cuatro"]
            logging = "off"
            result = nttt.acknowledgements.add_volunteer_acknowledgement(
                csv_file_path, output_file_path, language, volunteers, logging)
            self.assertTrue(result)

            # Check contents of final_step.md.
            contents = output_file_path.read_text()
            expected_contents = '\n'.join(["",
                                           "***",
                                           self.FIRST_LINE,
                                           "",
                                           "Volunteer One",
                                           "",
                                           "Vrijwilliger Twee",
                                           "",
                                           "Freiwillige Drei",
                                           "",
                                           "Voluntario Cuatro",
                                           "",
                                           self.LAST_LINE,
                                           ""])
            self.assertEqual(contents, expected_contents)

    def test_contents_preserved(self):
        '''
        Test case for the situation where the output file has contents that
        have to be preserved.
        '''

        with TemporaryDirectory() as temp_folder:
            data_folder = Path(os.getcwd(), "unit_test", "data")
            self.assertTrue(
                data_folder.is_dir(),
                "Subdirectory data of directory unit_test is missing.")
            csv_file_path = Path(data_folder, "volunteer_acknowledgements.csv")
            output_file_path = Path(temp_folder, "final_step.md")
            output_file_path.write_text("Line One.\nLine 2,\nline three.\n")
            language = "nl-NL"
            volunteers = ["Volunteer One"]
            logging = "off"
            result = nttt.acknowledgements.add_volunteer_acknowledgement(
                csv_file_path, output_file_path, language, volunteers, logging)
            self.assertIsNotNone(result)

            # Check contents of final_step.md.
            contents = output_file_path.read_text()
            expected_contents = '\n'.join(["Line One.",
                                           "Line 2,",
                                           "line three.",
                                           "***",
                                           self.FIRST_LINE,
                                           "",
                                           "Volunteer One",
                                           "",
                                           self.LAST_LINE,
                                           ""])
            self.assertEqual(contents, expected_contents)

    def test_trailing_blanks_removed(self):
        '''
        Test case for the situation where the output file has contents that
        have to be preserved, except for trailing blanks.
        '''

        with TemporaryDirectory() as temp_folder:
            data_folder = Path(os.getcwd(), "unit_test", "data")
            self.assertTrue(
                data_folder.is_dir(),
                "Subdirectory data of directory unit_test is missing.")
            csv_file_path = Path(data_folder, "volunteer_acknowledgements.csv")
            output_file_path = Path(temp_folder, "final_step.md")
            output_file_path.write_text("This is the end.\n\n    \n\n\t\n\n")
            language = "nl-NL"
            volunteers = ["Volunteer One"]
            logging = "off"
            result = nttt.acknowledgements.add_volunteer_acknowledgement(
                csv_file_path, output_file_path, language, volunteers, logging)
            self.assertIsNotNone(result)

            # Check contents of final_step.md.
            contents = output_file_path.read_text()
            expected_contents = '\n'.join(["This is the end.",
                                           "***",
                                           self.FIRST_LINE,
                                           "",
                                           "Volunteer One",
                                           "",
                                           self.LAST_LINE,
                                           ""])
            self.assertEqual(contents, expected_contents)

    def test_existing_acknowledgement(self):
        '''
        Test case for the situation where the acknowledgement already exists
        in the final step file.
        '''

        with TemporaryDirectory() as temp_folder:
            data_folder = Path(os.getcwd(), "unit_test", "data")
            self.assertTrue(
                data_folder.is_dir(),
                "Subdirectory data of directory unit_test is missing.")
            csv_file_path = Path(data_folder, "volunteer_acknowledgements.csv")
            output_file_path = Path(temp_folder, "final_step.md")
            output_file_path.touch()
            language = "nl-NL"
            volunteers = ["Volunteer One"]
            logging = "off"
            result = nttt.acknowledgements.add_volunteer_acknowledgement(
                csv_file_path, output_file_path, language, volunteers, logging)
            self.assertTrue(result)

            # Check contents of final_step.md.
            contents = output_file_path.read_text()
            expected_contents = '\n'.join(["",
                                           "***",
                                           self.FIRST_LINE,
                                           "",
                                           "Volunteer One",
                                           "",
                                           self.LAST_LINE,
                                           ""])
            self.assertEqual(contents, expected_contents)

            # Run again (using other volunteer names).
            volunteers = ["Vrijwilliger Twee", "Freiwillige Drei"]
            result = nttt.acknowledgements.add_volunteer_acknowledgement(
                csv_file_path, output_file_path, language, volunteers, logging)
            self.assertFalse(result)

            # Check contents of final_step.md - should not be changed.
            contents = output_file_path.read_text()
            self.assertEqual(contents, expected_contents)


if __name__ == "__main__":
    unittest.main()
