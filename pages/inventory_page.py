from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class InventoryPage:
    URL = "https://www.saucedemo.com/inventory.html"

    ITEM_TITLE = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")
    ADD_TO_CART_BTN = (By.CLASS_NAME, "btn_inventory")
    SELECT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    CART_ICON = (By.CLASS_NAME, "shopping_cart_link")

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
       # titles  = self.driver.find_elements(*self.ITEM_TITLE)
        list_titles = []
        '''
        for title in titles:
            list_titles.append(title.text)

        return list_titles
        '''

        return [title.text for title in titles]

    def add_to_cart(self):
        self.wait.until(EC.element_to_be_clickable(self.ADD_TO_CART_BTN)).click()


    def get_cart_number(self):
        cart = self.wait.until(EC.presence_of_element_located(self.CART_ICON))
        return cart.find_element(By.CLASS_NAME, "shopping_cart_badge").text

    def click_cart(self):
        self.wait.until(EC.element_to_be_clickable(self.CART_ICON)).click()

    def prep_to_checkout(self):
        buttons = self.wait.until(EC.presence_of_all_elements_located (self.ADD_TO_CART_BTN))
        buttons[0].click()
        buttons[1].click()
        buttons[2].click()
        self.wait.until(EC.element_to_be_clickable(self.CART_ICON)).click()


