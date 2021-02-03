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

        data_folder = Path(os.getcwd(), "unit_test", "data")
        self.assertTrue(data_folder.is_dir(),
                        "Subdirectory data of directory unit_test is missing.")
        csv_file_path = Path(data_folder, "volunteer_acknowledgements.csv")
        language = "nl-BE"
        result = nttt.acknowledgements.get_volunteer_acknowledgement(
            csv_file_path, language)
        self.assertIsNone(result)

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
            self.assertIsNotNone(result)

            # Check contents of final_step.md.
            contents = output_file_path.read_text()
            lines = contents.splitlines()
            self.assertEqual(11, len(lines))
            self.assertEqual("", lines[0])
            self.assertEqual("", lines[1])
            self.assertEqual(self.FIRST_LINE, lines[2])
            self.assertEqual("", lines[3])
            self.assertEqual("[name]", lines[4])
            self.assertEqual("", lines[5])
            self.assertEqual("[name]", lines[6])
            self.assertEqual("", lines[7])
            self.assertEqual("[name]", lines[8])
            self.assertEqual("", lines[9])
            self.assertEqual(self.LAST_LINE, lines[10])

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
            self.assertIsNotNone(result)

            # Check contents of final_step.md.
            contents = output_file_path.read_text()
            lines = contents.splitlines()
            self.assertEqual(7, len(lines))
            self.assertEqual("", lines[0])
            self.assertEqual("", lines[1])
            self.assertEqual(self.FIRST_LINE, lines[2])
            self.assertEqual("", lines[3])
            self.assertEqual("Volunteer One", lines[4])
            self.assertEqual("", lines[5])
            self.assertEqual(self.LAST_LINE, lines[6])

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
            self.assertIsNotNone(result)

            # Check contents of final_step.md.
            contents = output_file_path.read_text()
            lines = contents.splitlines()
            self.assertEqual(13, len(lines))
            self.assertEqual("", lines[0])
            self.assertEqual("", lines[1])
            self.assertEqual(self.FIRST_LINE, lines[2])
            self.assertEqual("", lines[3])
            self.assertEqual("Volunteer One", lines[4])
            self.assertEqual("", lines[5])
            self.assertEqual("Vrijwilliger Twee", lines[6])
            self.assertEqual("", lines[7])
            self.assertEqual("Freiwillige Drei", lines[8])
            self.assertEqual("", lines[9])
            self.assertEqual("Voluntario Cuatro", lines[10])
            self.assertEqual("", lines[11])
            self.assertEqual(self.LAST_LINE, lines[12])

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
            lines = contents.splitlines()
            self.assertEqual(9, len(lines))
            self.assertEqual("Line One.", lines[0])
            self.assertEqual("Line 2,", lines[1])
            self.assertEqual("line three.", lines[2])
            self.assertEqual("", lines[3])
            self.assertEqual(self.FIRST_LINE, lines[4])
            self.assertEqual("", lines[5])
            self.assertEqual("Volunteer One", lines[6])
            self.assertEqual("", lines[7])
            self.assertEqual(self.LAST_LINE, lines[8])

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
            lines = contents.splitlines()
            self.assertEqual(7, len(lines))
            self.assertEqual("This is the end.", lines[0])
            self.assertEqual("", lines[1])
            self.assertEqual(self.FIRST_LINE, lines[2])
            self.assertEqual("", lines[3])
            self.assertEqual("Volunteer One", lines[4])
            self.assertEqual("", lines[5])
            self.assertEqual(self.LAST_LINE, lines[6])


if __name__ == "__main__":
    unittest.main()
