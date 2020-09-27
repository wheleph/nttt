import os
import tempfile
import unittest
import nttt


class CustomNamedTemporaryFile:
    """
    This custom implementation is needed because of the following limitation of tempfile.NamedTemporaryFile:

    > Whether the name can be used to open the file a second time, while the named temporary file is still open,
    > varies across platforms (it can be so used on Unix; it cannot on Windows NT or later).
    """
    def __init__(self, mode='wb', delete=True):
        self._mode = mode
        self._delete = delete

    def __enter__(self):
        # Generate a random temporary file name
        file_name = os.path.join(tempfile.gettempdir(), os.urandom(24).hex())
        # Ensure the file is created
        open(file_name, "x").close()
        # Open the file in the given mode
        self._tempFile = open(file_name, self._mode)
        return self._tempFile

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._tempFile.close()
        if self._delete:
            os.remove(self._tempFile.name)


class AssertHelper:
    @staticmethod
    def assert_fix_meta(input_file_content, english_content, expected_output_file_content):
        """
        - Prepare input file
        - Run nttt.tidyup.fix_meta
        - Assert that the output file has the expected content
        """
        with CustomNamedTemporaryFile(mode="wb", delete=True) as temp_src, \
                CustomNamedTemporaryFile(mode="wb", delete=True) as temp_english_src, \
                CustomNamedTemporaryFile(mode="rb", delete=True) as temp_dest:
            temp_src.write(input_file_content.encode('utf-8'))
            temp_src.flush()

            temp_english_src.write(english_content.encode('utf-8'))
            temp_english_src.flush()

            nttt.tidyup.fix_meta(temp_src.name, temp_english_src.name, temp_dest.name)

            result = temp_dest.read().decode('utf-8')
            unittest.TestCase().assertEqual(result, expected_output_file_content)

    @staticmethod
    def assert_fix_step(input_file_content, second_argument, expected_output_file_content):
        """
        - Prepare input file
        - Run nttt.tidyup.fix_step
        - Assert that the output file has the expected content
        """
        with CustomNamedTemporaryFile(mode="wb", delete=True) as temp_src, \
                CustomNamedTemporaryFile(mode="rb", delete=True) as temp_dest:
            temp_src.write(input_file_content.encode('utf-8'))
            temp_src.flush()

            nttt.tidyup.fix_md_step(temp_src.name, second_argument, temp_dest.name, (), "off")

            result = temp_dest.read().decode('utf-8')
            unittest.TestCase().assertEqual(result, expected_output_file_content)