import unittest
from bs4 import BeautifulSoup
from export_data import clean_cell_value

class TestExportData(unittest.TestCase):
    def test_clean_cell_value_html(self):
        html_input = "<td>Hello<br>World&amp;Co.</td>"
        soup = BeautifulSoup(html_input, "html.parser").find("td")
        cleaned = clean_cell_value(soup)
        self.assertIn("Hello", cleaned)
        self.assertIn("World&Co.", cleaned)

    def test_clean_cell_value_empty(self):
        self.assertEqual(clean_cell_value(None), "")
        self.assertEqual(clean_cell_value(""), "")

if __name__ == "__main__":
    unittest.main()
