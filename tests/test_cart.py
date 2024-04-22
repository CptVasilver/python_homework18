import allure
import requests
from selene import browser, have
from allure_commons._allure import step
from allure_commons.types import AttachmentType
from tests.conftest import get_cookie




LOGIN = "vasilver.work@yandex.ru"
PASSWORD = "RainbowClown2"
URL = "https://demowebshop.tricentis.com"
# def add_product():

def test_add_products_to_cart():

    cookie = get_cookie()

    with step('Set cookie'):
        browser.open('/')
        browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie})
        browser.open('/')
