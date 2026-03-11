from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

class BasePage:
    """Basis-Klasse für alle Page Objects."""
    def __init__(self, driver):
        self.driver = driver
        self.timeout = 30

    def wait_for_element(self, locator):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located(locator)
        )

    def click(self, locator):
        element = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()

    def get_text(self, locator):
        element = self.wait_for_element(locator)
        return element.text

    def take_screenshot(self, name):
        artifact_dir = os.path.join(os.path.dirname(__file__), "..", "selenium_artifacts")
        if not os.path.exists(artifact_dir):
            os.makedirs(artifact_dir)
        path = os.path.join(artifact_dir, f"{name}.png")
        self.driver.save_screenshot(path)
        print(f"Screenshot saved to: {path}")
