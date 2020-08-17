import unittest
import nttt
from pathlib import Path
from tempfile import TemporaryDirectory


class FileSystemTest(unittest.TestCase):

    def test_find_missing_entries(self):
        '''Test case for the find_missing_entries function.'''

        with TemporaryDirectory() as temp_folder:
            # Empty source and destination folders.
            source_folder = Path(temp_folder, "source")
            source_folder.mkdir()
            dest_folder = Path(temp_folder, "dest")
            dest_folder.mkdir()
            (missing_folders, missing_files) = nttt.utilities.find_missing_entries(source_folder, dest_folder)
            self.assertEqual(missing_folders, [])
            self.assertEqual(missing_files, [])

            # Add folders and files to source folder.
            Path(source_folder, "folder_1").mkdir()
            Path(source_folder, "folder_2").mkdir()
            Path(source_folder, "file_1").touch()
            Path(source_folder, "file_2").touch()
            Path(source_folder, "file_3").touch()
            Path(source_folder, ".keep").touch()
            (missing_folders, missing_files) = nttt.utilities.find_missing_entries(source_folder, dest_folder)
            self.assertEqual(sorted(missing_folders), ["folder_1", "folder_2"])
            self.assertEqual(sorted(missing_files), [".keep", "file_1", "file_2", "file_3"])

            # Add some files to the subfolders.
            Path(source_folder, "folder_1", "file_4").touch()
            Path(source_folder, "folder_1", "file_5").touch()
            Path(source_folder, "folder_2", "file_6").touch()
            (missing_folders, missing_files) = nttt.utilities.find_missing_entries(source_folder, dest_folder)
            self.assertEqual(sorted(missing_folders), ["folder_1", "folder_2"])
            self.assertEqual(sorted(missing_files), [".keep", "file_1", "file_2", "file_3"])

            # Add some of the folders and files to destination folder.
            Path(dest_folder, "folder_1").mkdir()
            Path(dest_folder, "file_1").touch()
            (missing_folders, missing_files) = nttt.utilities.find_missing_entries(source_folder, dest_folder)
            self.assertEqual(sorted(missing_folders), ["folder_2"])
            self.assertEqual(sorted(missing_files), [".keep", "file_2", "file_3"])

            # Add the other folders and files to destination folder.
            Path(dest_folder, "folder_2").mkdir()
            Path(dest_folder, "file_2").touch()
            Path(dest_folder, "file_3").touch()
            Path(dest_folder, ".keep").touch()
            (missing_folders, missing_files) = nttt.utilities.find_missing_entries(source_folder, dest_folder)
            self.assertEqual(missing_folders, [])
            self.assertEqual(missing_files, [])

            # Add some extra folders and files to destination folder.
            Path(dest_folder, "folder_3").mkdir()
            Path(dest_folder, "folder_3", "file_7").touch()
            Path(dest_folder, "file_8").touch()
            (missing_folders, missing_files) = nttt.utilities.find_missing_entries(source_folder, dest_folder)
            self.assertEqual(missing_folders, [])
            self.assertEqual(missing_files, [])

    def test_copy_missing_folders(self):
        '''Test case for the copy_missing_folders function.'''

        with TemporaryDirectory() as temp_folder:
            source_folder = Path(temp_folder, "source")
            source_folder.mkdir()
            dest_folder = Path(temp_folder, "dest")
            dest_folder.mkdir()
            Path(source_folder, "folder_1").mkdir()
            Path(source_folder, "folder_2").mkdir()
            Path(source_folder, "folder_3").mkdir()
            Path(source_folder, "folder_1", "file_1").write_text("This is the first file\n")
            Path(source_folder, "folder_1", "file_2").write_text("This is\nthe second file\n")
            Path(source_folder, "folder_2", "file_3").write_text("This is\nthe third\nfile\n")
            Path(source_folder, "folder_3", ".keep").touch()
            folders_to_copy = ["folder_1", "folder_3"]
            nttt.utilities.copy_missing_folders(source_folder, folders_to_copy, dest_folder)
            self.assertTrue(Path(dest_folder, "folder_1").is_dir())
            self.assertFalse(Path(dest_folder, "folder_2").exists())
            self.assertTrue(Path(dest_folder, "folder_3").is_dir())
            self.assertTrue(Path(dest_folder, "folder_1", "file_1").is_file())
            self.assertTrue(Path(dest_folder, "folder_1", "file_2").is_file())
            self.assertTrue(Path(dest_folder, "folder_3", ".keep").is_file())
            self.assertEqual(Path(dest_folder, "folder_1", "file_1").read_text(), "This is the first file\n")
            self.assertEqual(Path(dest_folder, "folder_1", "file_2").read_text(), "This is\nthe second file\n")
            self.assertEqual(Path(dest_folder, "folder_3", ".keep").read_text(), "")

    def test_copy_missing_files(self):
        '''Test case for the copy_missing_files function.'''

        with TemporaryDirectory() as temp_folder:
            source_folder = Path(temp_folder, "source")
            source_folder.mkdir()
            dest_folder = Path(temp_folder, "dest")
            dest_folder.mkdir()
            Path(source_folder, "file_1").write_text("This is the first file\n")
            Path(source_folder, "file_2").write_text("This is\nthe second file\n")
            Path(source_folder, "file_3").write_text("This is\nthe third\nfile\n")
            files_to_copy = ["file_1", "file_3"]
            nttt.utilities.copy_missing_files(source_folder, files_to_copy, dest_folder)
            self.assertTrue(Path(dest_folder, "file_1").is_file())
            self.assertFalse(Path(dest_folder, "file_2").exists())
            self.assertTrue(Path(dest_folder, "file_3").is_file())
            self.assertEqual(Path(dest_folder, "file_1").read_text(), "This is the first file\n")
            self.assertEqual(Path(dest_folder, "file_3").read_text(), "This is\nthe third\nfile\n")

    def test_add_missing_entries(self):
        '''Test case for the add_missing_entries function.'''

        with TemporaryDirectory() as temp_folder:
            input_folder = Path(temp_folder, "input")
            input_folder.mkdir()
            english_folder = Path(temp_folder, "english")
            english_folder.mkdir()
            output_folder = Path(temp_folder, "output")
            output_folder.mkdir()
            Path(input_folder, "folder_1").mkdir()
            Path(input_folder, "folder_2").mkdir()
            Path(input_folder, "folder_3").mkdir()
            Path(input_folder, "folder_1", "file_1").write_text("This is the first file\n")
            Path(input_folder, "folder_1", "file_2").write_text("This is\nthe second file\n")
            Path(input_folder, "folder_2", "file_3").write_text("This is\nthe third\nfile\n")
            Path(input_folder, "folder_3", ".keep").touch()
            Path(input_folder, "file_4").write_text("Fourth file")
            Path(input_folder, "file_5").write_text("File number 5")
            Path(english_folder, "folder_4").mkdir()
            Path(english_folder, "folder_5").mkdir()
            Path(english_folder, "folder_4", "file_6").write_text("This is the sixth file\n")
            Path(english_folder, "folder_5", ".keep").touch()
            Path(english_folder, "file_7").write_text("File\n7\n")
            Path(output_folder, "folder_1").mkdir()
            Path(output_folder, "folder_4").mkdir()
            Path(output_folder, "folder_1", "file_1").write_text("File one")
            Path(output_folder, "file_4").write_text("File four")
            # Expectations:
            # - folder_1 exists at the destination, so folder_1/file_2 is not
            #   copied to the destination
            # - folder_2 and folder_3 do not exist at the destination, so these
            #   folders are created at the destination and folder_2/file3 and
            #   folder_3/.keep are copied to the destination
            # - file_4 exists at the destination, so it is not copied
            # - file_5 does not exist at the destination, so it is copied to
            #   the destination
            # - folder_4 exists at the destination, so folder_4/file_6 is not
            #   copied to the destination
            # - folder_5 does not exist at the destination, so this folder is
            #   created at the destination and folder_5/.keep is copied to the
            #   destination
            # - file_7 does not exist at the destination, but is should not be
            #   copied to the destination
            nttt.utilities.add_missing_entries(input_folder, english_folder, output_folder)
            self.assertFalse(Path(output_folder, "folder_1", "file_2").exists())
            self.assertTrue(Path(output_folder, "folder_2", "file_3").is_file())
            self.assertTrue(Path(output_folder, "folder_3", ".keep").is_file())
            self.assertTrue(Path(output_folder, "file_5").is_file())
            self.assertEqual(Path(output_folder, "folder_2", "file_3").read_text(), "This is\nthe third\nfile\n")
            self.assertEqual(Path(output_folder, "folder_3", ".keep").read_text(), "")
            self.assertFalse(Path(output_folder, "folder_4", "file_6").exists())
            self.assertTrue(Path(output_folder, "folder_5", ".keep").is_file())
            self.assertFalse(Path(output_folder, "file_7").exists())
            self.assertEqual(Path(output_folder, "folder_5", ".keep").read_text(), "")


if __name__ == "__main__":
    unittest.main()
