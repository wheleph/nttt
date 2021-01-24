import unittest
from nttt import cleanup_sections


class TestCleanupSections(unittest.TestCase):
    logging = "off"

    def test_remove_backslashes(self):
        c_initial = '''\\--- task \\---

Wat gebeurt er als de boot de muisaanwijzer bereikt? Probeer het uit om te zien wat het probleem is.

\\--- /task \\---'''
        c_target = '''--- task ---

Wat gebeurt er als de boot de muisaanwijzer bereikt? Probeer het uit om te zien wat het probleem is.

--- /task ---'''
        self.assertEqual(cleanup_sections.fix_sections(c_initial, self.logging), c_target)

    def test_fix_hints(self):
        c_initial = '''\\--- hints \\--- \\--- hint \\---

De boot mag alleen naar de muisaanwijzer wijzen en bewegen `als>`{:class="block3control"} de `afstand tot muisaanwijzer`{:class="block3sensing"} `groter dan 5 pixels`{:class="block3operators"} is.

\\--- /hint \\--- \\--- hint \\---

Dit zijn de code blokken die je moet toevoegen aan de code voor de boot-sprite:

\\--- /hint \\--- \\--- hint \\---

Dit is hoe je code eruit zou moeten zien:

\\--- /hint \\--- \\--- /hints \\---'''
        c_target = '''--- hints ---
--- hint ---

De boot mag alleen naar de muisaanwijzer wijzen en bewegen `als>`{:class="block3control"} de `afstand tot muisaanwijzer`{:class="block3sensing"} `groter dan 5 pixels`{:class="block3operators"} is.

--- /hint ---
--- hint ---

Dit zijn de code blokken die je moet toevoegen aan de code voor de boot-sprite:

--- /hint ---
--- hint ---

Dit is hoe je code eruit zou moeten zien:

--- /hint ---
--- /hints ---'''
        self.assertEqual(cleanup_sections.fix_sections(c_initial, self.logging), c_target)

    def test_fix_title(self):
        c_initial = '''## \\--- collapse \\---

## title: Нотатки керівника клубу

## Вступ:
'''
        c_target = '''--- collapse ---
---
title: Нотатки керівника клубу
---

## Вступ:
'''
        self.assertEqual(cleanup_sections.fix_sections(c_initial, self.logging), c_target)


if __name__ == '__main__':
    unittest.main()
