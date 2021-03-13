import unittest
from nttt import cleanup_sections


class TestCleanupSections(unittest.TestCase):
    logging = "off"

    def test_remove_backslashes(self):
        c_initial = ("\\--- task \\---\n"
                     "\n"
                     "Wat gebeurt er als de boot de muisaanwijzer bereikt? Probeer het uit om te zien wat het probleem is.\n"
                     "\n"
                     "\\--- /task \\---")

        c_target = ("--- task ---\n"
                    "\n"
                    "Wat gebeurt er als de boot de muisaanwijzer bereikt? Probeer het uit om te zien wat het probleem is.\n"
                    "\n"
                    "--- /task ---")

        self.assertEqual(cleanup_sections.fix_sections(c_initial, self.logging), c_target)

    def test_fix_missing_spaces(self):
        c_initial = ("\\---task \\---\n"
                     "\n"
                     "Wat gebeurt er als de boot de muisaanwijzer bereikt? Probeer het uit om te zien wat het probleem is.\n"
                     "\n"                     
                     "\\--- /task\\---")

        c_target = ("--- task ---\n"
                    "\n"
                    "Wat gebeurt er als de boot de muisaanwijzer bereikt? Probeer het uit om te zien wat het probleem is.\n"
                    "\n"                    
                    "--- /task ---")

        self.assertEqual(cleanup_sections.fix_sections(c_initial, self.logging), c_target)

    def test_fix_double_dash(self):
        c_initial = ("--task --\n"
                     "\n"
                     "Wat gebeurt er als de boot de muisaanwijzer bereikt? Probeer het uit om te zien wat het probleem is.\n"
                     "\n"                     
                     "-- /task\\---")

        c_target = ("--- task ---\n"
                    "\n"
                    "Wat gebeurt er als de boot de muisaanwijzer bereikt? Probeer het uit om te zien wat het probleem is.\n"
                    "\n"
                    "--- /task ---")

        self.assertEqual(cleanup_sections.fix_sections(c_initial, self.logging), c_target)

    def test_fix_hints(self):
        c_initial = ('\\--- hints \\--- \\--- hint \\---\n'
                     '\n'
                     'De boot mag alleen naar de muisaanwijzer wijzen en bewegen `als>`{:class="block3control"} de `afstand tot muisaanwijzer`{:class="block3sensing"} `groter dan 5 pixels`{:class="block3operators"} is.\n'
                     '\n'
                     '\\--- /hint \\--- \\--- hint \\---\n'
                     '\n'
                     'Dit zijn de code blokken die je moet toevoegen aan de code voor de boot-sprite:\n'
                     '\n'
                     '\\--- /hint \\--- \\--- hint \\---\n'
                     '\n'
                     'Dit is hoe je code eruit zou moeten zien:\n'
                     '\n'
                     '\\--- /hint \\--- \\--- /hints \\---')
        c_target = ('--- hints ---\n'
                    '--- hint ---\n'
                    '\n'
                    'De boot mag alleen naar de muisaanwijzer wijzen en bewegen `als>`{:class="block3control"} de `afstand tot muisaanwijzer`{:class="block3sensing"} `groter dan 5 pixels`{:class="block3operators"} is.\n'
                    '\n'
                    '--- /hint ---\n'
                    '--- hint ---\n'
                    '\n'
                    'Dit zijn de code blokken die je moet toevoegen aan de code voor de boot-sprite:\n'
                    '\n'
                    '--- /hint ---\n'
                    '--- hint ---\n'
                    '\n'
                    'Dit is hoe je code eruit zou moeten zien:\n'
                    '\n'
                    '--- /hint ---\n'
                    '--- /hints ---')

        self.assertEqual(cleanup_sections.fix_sections(c_initial, self.logging), c_target)

    def test_fix_task(self):
        c_initial = ('\\--- task \\--- \\--- hints \\--- \\--- hint \\---\n'
                     '\\--- /hint \\--- \\--- /hints \\--- \\--- /task \\---')
        c_target = ('--- task ---\n'
                    '--- hints ---\n'
                    '--- hint ---\n'
                    '--- /hint ---\n'
                    '--- /hints ---\n'
                    '--- /task ---')

        self.assertEqual(cleanup_sections.fix_sections(c_initial, self.logging), c_target)

    def test_fix_title(self):
        c_initial = ('## \\--- collapse \\---\n'
                     '\n'
                     '## title: Нотатки керівника клубу\n'
                     '\n'
                     '## Вступ:\n')

        c_target = ('--- collapse ---\n'
                    '---\n'
                    'title: Нотатки керівника клубу\n'
                    '---\n'
                    '\n'
                    '## Вступ:\n')
        self.assertEqual(cleanup_sections.fix_sections(c_initial, self.logging), c_target)

    def test_fix_title_translated(self):
        c_initial = ('## \\--- collapse \\---\n'
                     '\n'
                     '## Назва: Нотатки керівника клубу\n'
                     '\n'
                     '## Вступ:\n')

        c_target = ('--- collapse ---\n'
                    '---\n'
                    'title: Нотатки керівника клубу\n'
                    '---\n'
                    '\n'
                    '## Вступ:\n')
        self.assertEqual(cleanup_sections.fix_sections(c_initial, self.logging), c_target)


    def test_fix_translation_mismatch(self):
        c_initial = ('--- wenken ---\n'
                     '--- wenk ---\n'
                     '\n'
                     'De boot mag alleen naar de muisaanwijzer wijzen en bewegen `als>`{:class="block3control"} de `afstand tot muisaanwijzer`{:class="block3sensing"} `groter dan 5 pixels`{:class="block3operators"} is.\n'
                     '\n'
                     '--- /hint ---\n'
                     '--- wenk ---\n'
                     '\n'
                     'Dit zijn de code blokken die je moet toevoegen aan de code voor de boot-sprite:\n'
                     '\n'
                     '--- /wenk ---\n'
                     '--- hint ---\n'
                     '\n'
                     'Dit is hoe je code eruit zou moeten zien:\n'
                     '\n'
                     '--- /hint ---\n'
                     '--- /hints ---')
        c_original = ('--- hints ---\n'
                      '--- hint ---\n'
                      '\n'
                      'The boat should only point towards the mouse pointer and move `if`{:class="block3control"} the `distance to the mouse pointer`{:class="block3sensing"} is `greater than 5 pixels`{:class="block3operators"}.\n'
                      '\n'
                      '--- /hint ---\n'
                      '--- hint ---\n'
                      '\n'
                      'These are the code blocks you need to add to the code for the boat sprite:\n'
                      '\n'
                      '--- /hint ---\n'
                      '--- /hints ---')
        c_target = ('--- wenken ---\n'
                    '--- wenk ---\n'
                    '\n'
                    'De boot mag alleen naar de muisaanwijzer wijzen en bewegen `als>`{:class="block3control"} de `afstand tot muisaanwijzer`{:class="block3sensing"} `groter dan 5 pixels`{:class="block3operators"} is.\n'
                    '\n'
                    '--- /hint ---\n'
                    '--- wenk ---\n'
                    '\n'
                    'Dit zijn de code blokken die je moet toevoegen aan de code voor de boot-sprite:\n'
                    '\n'
                    '--- /wenk ---\n'
                    '--- hint ---\n'
                    '\n'
                    'Dit is hoe je code eruit zou moeten zien:\n'
                    '\n'
                    '--- /hint ---\n'
                    '--- /hints ---')

        self.assertEqual(cleanup_sections.revert_section_translation("step_1.md", c_initial, c_original, self.logging), c_target)

    def test_fix_translation_match(self):
        c_initial = ('--- wenken ---\n'
                     '--- wenk ---\n'
                     '\n'
                     'De boot mag alleen naar de muisaanwijzer wijzen en bewegen `als>`{:class="block3control"} de `afstand tot muisaanwijzer`{:class="block3sensing"} `groter dan 5 pixels`{:class="block3operators"} is.\n'
                     '\n'
                     'Extra line\n'
                     '--- /hint ---\n'
                     '--- wenk ---\n'
                     '\n'
                     'Dit zijn de code blokken die je moet toevoegen aan de code voor de boot-sprite:\n'
                     '\n'
                     '--- /wenk ---\n'
                     '--- hint ---\n'
                     '\n'
                     'Dit is hoe je code eruit zou moeten zien:\n'
                     '\n'
                     '--- /hint ---\n'
                     '--- /hints ---')
        c_original = ('--- hints ---\n'
                      '--- hint ---\n'
                      '\n'
                      'The boat should only point towards the mouse pointer and move `if`{:class="block3control"} the `distance to the mouse pointer`{:class="block3sensing"} is `greater than 5 pixels`{:class="block3operators"}.\n'
                      '\n'
                      '--- /hint ---\n'
                      '--- hint ---\n'
                      '\n'
                      'These are the code blocks you need to add to the code for the boat sprite:\n'
                      '\n'
                      '--- /hint ---\n'
                      '--- hint ---\n'
                      '\n'
                      'This is what your code should look like:\n'
                      '\n'
                      '--- /hint ---\n'
                      '--- /hints ---')
        c_target = ('--- hints ---\n'
                    '--- hint ---\n'
                    '\n'
                    'De boot mag alleen naar de muisaanwijzer wijzen en bewegen `als>`{:class="block3control"} de `afstand tot muisaanwijzer`{:class="block3sensing"} `groter dan 5 pixels`{:class="block3operators"} is.\n'
                    '\n'
                    'Extra line\n'
                    '--- /hint ---\n'
                    '--- hint ---\n'
                    '\n'
                    'Dit zijn de code blokken die je moet toevoegen aan de code voor de boot-sprite:\n'
                    '\n'
                    '--- /hint ---\n'
                    '--- hint ---\n'
                    '\n'
                    'Dit is hoe je code eruit zou moeten zien:\n'
                    '\n'
                    '--- /hint ---\n'
                    '--- /hints ---')

        self.assertEqual(cleanup_sections.revert_section_translation("step_1.md", c_initial, c_original, self.logging), c_target)


if __name__ == '__main__':
    unittest.main()
