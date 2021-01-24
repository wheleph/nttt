from .utilities import find_snippet
from .nttt_logging import log_replacement


# TODO think about logging of these replacements
def fix_sections(md_file_content, logging):
    # For some weird reason Crowdin replaces '---' to '\---' in its output. So let's revert it back
    md_file_content = md_file_content.replace("\\---", "---")

    # For some weird reason Crowdin jams 'hints' and 'hint' tags into one line it its output.
    # Probably because they go in adjacent lines (no empty line between them).
    # So let's revert it back
    md_file_content = md_file_content.replace("--- hints --- --- hint ---", "--- hints ---\n--- hint ---")
    md_file_content = md_file_content.replace("--- /hint --- --- hint ---", "--- /hint ---\n--- hint ---")
    md_file_content = md_file_content.replace("--- /hint --- --- /hints ---", "--- /hint ---\n--- /hints ---")

    # For some weird reason Crowdin breaks 'title' tags. So let's revert it back
    collapse_error = "## --- collapse ---\n\n## title: "
    collapse_title = find_snippet(md_file_content, collapse_error, "\n")
    while collapse_title is not None:
        original_text = collapse_error + collapse_title + "\n"
        replacement_text = "--- collapse ---\n---\ntitle: " + collapse_title + "\n---\n"
        md_file_content = md_file_content.replace(original_text, replacement_text)
        log_replacement(original_text, replacement_text, logging)

        collapse_title = find_snippet(md_file_content, collapse_error, "\n")

    return md_file_content
