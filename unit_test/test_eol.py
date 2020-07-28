import unittest
import tempfile
import nttt


class TestEol(unittest.TestCase):
    def test_fix_metadata_crlf(self):
        self.helper_test_fix_metadata(
            "---\r\n"
            "steps:\r\n"
            "  - \r\n"
            "    title: Inleiding\r\n",
            "---\r\n"
            "steps:\r\n"
            "  - title: Inleiding\r\n")

    @unittest.skip("should be fixed later")
    def test_fix_metadata_lf(self):
        self.helper_test_fix_metadata(
                          "---\n"
                          "steps:\n"
                          "  - \n"
                          "    title: Inleiding\n",
                          "---\n"
                          "steps:\n"
                          "  - title: Inleiding\n")

    def helper_test_fix_metadata(self, input_file_content, expected_output_file_content):
        with tempfile.NamedTemporaryFile(mode="wb") as temp_src, \
                tempfile.NamedTemporaryFile(mode="rb") as temp_dest:
            temp_src.write(input_file_content.encode('utf-8'))
            temp_src.flush()

            nttt.tidyup.fix_meta(temp_src.name, temp_dest.name)

            result = temp_dest.read().decode('utf-8')
            self.assertEqual(result, expected_output_file_content)


if __name__ == '__main__':
    unittest.main()
