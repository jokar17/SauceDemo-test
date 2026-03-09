from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class InformationPage:

    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    ZIP_INPUT = (By.ID, "postal-code")
    CANCEL_BTN = (By.XPATH, "//button[@data-test='cancel']")
    CONTINUE_BTN = (By.ID, "continue")
    ERROR_MSG = (By.XPATH, "//h3[@data-test='error']")


    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def fill_checkout_form(self, name=None, surname=None, zip=None):
        if name:
            self.wait.until(EC.visibility_of_element_located(self.FIRST_NAME_INPUT)).send_keys(name)
        if surname:
            self.wait.until(EC.visibility_of_element_located(self.LAST_NAME_INPUT)).send_keys(surname)
        if zip:
            self.wait.until(EC.visibility_of_element_located(self.ZIP_INPUT)).send_keys(zip)
        self.wait.until(EC.element_to_be_clickable(self.CONTINUE_BTN)).click()


    def click_cancel(self):
        self.wait.until(EC.element_to_be_clickable(self.CANCEL_BTN)).click()


    def get_error_message(self):
        return self.wait.until(EC.presence_of_element_located(self.ERROR_MSG)).text