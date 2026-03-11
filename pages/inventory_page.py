from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class InventoryPage:
    URL = "https://www.saucedemo.com/inventory.html"

    ITEM_TITLE = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")
    ADD_TO_CART_BTN = (By.CSS_SELECTOR, "[data-test^='add-to-cart']")
    SELECT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    CART_ICON = (By.CLASS_NAME, "shopping_cart_link")

    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")


    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get(self.URL)

    def select_order(self, orderValue):
        element = self.wait.until(EC.presence_of_element_located(self.SELECT_DROPDOWN))
        drop = Select(element)
        drop.select_by_value(orderValue)

    def get_titles_list(self):
        titles = self.wait.until(EC.presence_of_all_elements_located(self.ITEM_TITLE))
        return [title.text for title in titles]

    def add_to_cart(self):
        self.wait.until(EC.element_to_be_clickable(self.ADD_TO_CART_BTN)).click()


    def get_cart_number(self):
        cart = self.wait.until(EC.presence_of_element_located(self.CART_ICON))
        return cart.find_element(By.CLASS_NAME, "shopping_cart_badge").text

    def click_cart(self):
        self.wait.until(EC.element_to_be_clickable(self.CART_ICON)).click()

    '''
    def prep_to_checkout(self):
        buttons = self.wait.until(EC.presence_of_all_elements_located (self.ADD_TO_CART_BTN))
        for i in range(3):
            buttons = self.wait.until(EC.presence_of_all_elements_located(self.ADD_TO_CART_BTN))
            buttons[i].click()
        self.wait.until(EC.element_to_be_clickable(self.CART_ICON)).click()
        for _ in range(3):
            self.wait.until(EC.presence_of_element_located(self.ADD_TO_CART_BTN)).click()
        self.wait.until(EC.presence_of_element_located(self.CART_ICON)).click()
    '''

    REMOVE_BTN = (By.CSS_SELECTOR, "[data-test^='remove']")

    def prep_to_checkout(self):
        # debug: vediamo cosa c'è sulla pagina
        self.driver.save_screenshot("reports/screenshots/debug_before_click.png")

        for i in range(3):
            buttons = self.driver.find_elements(*self.ADD_TO_CART_BTN)
            print(f"--- Iterazione {i}: trovati {len(buttons)} bottoni add-to-cart ---")
            print(f"    URL: {self.driver.current_url}")

            if not buttons:
                self.driver.save_screenshot(f"reports/screenshots/debug_no_buttons_{i}.png")
                raise Exception(f"Nessun bottone add-to-cart trovato all'iterazione {i}")

            self.driver.execute_script("arguments[0].click();", buttons[0])

            WebDriverWait(self.driver, 10).until(
                lambda d, n=i + 1: self._badge_count(d) == n
            )

        self.wait.until(EC.element_to_be_clickable(self.CART_ICON)).click()


    def _badge_count(self, d):
        try:
            return int(d.find_element(*self.CART_BADGE).text)
        except:
            return 0

