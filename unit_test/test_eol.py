import unittest
import nttt
from unit_test.test_utilities import CustomNamedTemporaryFile


class TestEol(unittest.TestCase):
    def test_fix_metadata_crlf(self):
        self.assert_function_call(nttt.tidyup.fix_meta,
                                  "---\r\n"
                                  "steps:\r\n"
                                  "  - \r\n"
                                  "    title: Inleiding\r\n",

                                  "---\r\n"
                                  "steps:\r\n"
                                  "  - title: Inleiding\r\n")

    def test_fix_metadata_lf(self):
        self.assert_function_call(nttt.tidyup.fix_meta,
                                  "---\n"
                                  "steps:\n"
                                  "  - \n"
                                  "    title: Inleiding\n",

                                  "---\n"
                                  "steps:\n"
                                  "  - title: Inleiding\n")

    def test_fix_collapse_block_crlf(self):
        self.assert_function_call(nttt.tidyup.fix_step,
                                  "--- collapse ---\r\n"
                                  "\r\n"
                                  "## title: My title\r\n",

                                  "--- collapse ---\r\n"
                                  "---\r\n"
                                  "title: My title\r\n"
                                  "---\r\n")

    def test_fix_collapse_block_lf(self):
        self.assert_function_call(nttt.tidyup.fix_step,
                                  "--- collapse ---\n"
                                  "\n"
                                  "## title: My title\n",

                                  "--- collapse ---\n"
                                  "---\n"
                                  "title: My title\n"
                                  "---\n")

    def assert_function_call(self, func, input_file_content, expected_output_file_content):
        """
        - Prepare input file
        - Run the given function (that takes as arguments names of input and output files)
        - Assert that the output file has the expected content
        """
        with CustomNamedTemporaryFile(mode="wb", delete=True) as temp_src, \
                CustomNamedTemporaryFile(mode="rb", delete=True) as temp_dest:
            temp_src.write(input_file_content.encode('utf-8'))
            temp_src.flush()

            func(temp_src.name, temp_dest.name)

            result = temp_dest.read().decode('utf-8')
            self.assertEqual(result, expected_output_file_content)


if __name__ == '__main__':
    unittest.main()