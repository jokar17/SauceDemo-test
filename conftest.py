import pytest_html
from selenium import webdriver
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
import pytest
import os
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser su cui eseguire i test: chrome | firefox"
    )

@pytest.fixture()
def driver(request):
    browser = request.config.getoption("--browser")

    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        d = webdriver.Chrome(options=options)
    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        d = webdriver.Firefox(options=options)
    else:
        raise ValueError(f"Browser non supportato: {browser}")

    yield d
    d.quit()

@pytest.fixture()
def logged_driver(driver):
    page = LoginPage(driver)
    page.open()
    page.login("standard_user", "secret_sauce")

    WebDriverWait(driver, 10).until(
        EC.url_contains("inventory")
    )
    yield driver



@pytest.fixture()
def checkout_driver(logged_driver):
    page = InventoryPage(logged_driver)
    page.prep_to_checkout()

    WebDriverWait(logged_driver, 10).until(
        EC.url_contains("cart")
    )

    yield logged_driver


@pytest.fixture()
def information_driver(checkout_driver):
    page = CartPage(checkout_driver)
    page.click_checkout()

    WebDriverWait(checkout_driver, 10).until(
        EC.url_contains("checkout-step-one")
    )

    yield checkout_driver




@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("information_driver") or \
                 item.funcargs.get("checkout_driver") or \
                 item.funcargs.get("logged_driver") or \
                 item.funcargs.get("driver")

        if driver:
            os.makedirs("reports/screenshots", exist_ok=True)
            path = f"reports/screenshots/{item.name}.png"
            driver.save_screenshot(path)

            extras = getattr(report, "extras", [])
            extras.append(pytest_html.extras.image(path))
            report.extras = extras

def pytest_configure(config):
    config._metadata = getattr(config, "_metadata", {})
    browser = config.getoption("--browser", default="chrome", skip=True)
    config._metadata["Browser"] = browser
    config._metadata["Environment"] = "Test"
    config._metadata["URL"] = "https://www.saucedemo.com"