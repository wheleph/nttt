def fix_sections(md_file_content, logging):
    # For some weird reason Crowdin replaces '---' to '\---' in its output. So let's revert it back
    md_file_content = md_file_content.replace("\\---", "---")

    # For some weird reason Crowdin jams 'hints' and 'hint' tags into one line it its output.
    # Probably because they go in adjacent lines (no empty line between them).
    # So let's revert it back
    md_file_content = md_file_content.replace("--- hints --- --- hint ---", "--- hints ---\n--- hint ---")
    md_file_content = md_file_content.replace("--- /hint --- --- hint ---", "--- /hint ---\n--- hint ---")
    md_file_content = md_file_content.replace("--- /hint --- --- /hints ---", "--- /hint ---\n--- /hints ---")
    return md_file_content
