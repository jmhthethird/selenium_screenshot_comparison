"""Test Selenium functionality."""
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class PythonOrgSearch(unittest.TestCase):
    """Simple set of test for Selenium driver."""

    def setUp(self):
        """Construct test setup."""
        self.driver = webdriver.Chrome()

    def test_search_in_python_org(self):
        """Test basic navigation functions of driver."""
        driver = self.driver
        driver.get("http://www.python.org")
        self.assertIn("Python", driver.title)
        elem = driver.find_element_by_name("q")
        elem.send_keys("pycon")
        elem.send_keys(Keys.RETURN)
        assert "No results found." not in driver.page_source

    def tearDown(self):
        """Deconstruct test setup."""
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
