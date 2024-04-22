import allure
import requests
from selene import browser, have
from allure_commons._allure import step
from allure_commons.types import AttachmentType
from tests.conftest import get_cookie, clear_cart

LOGIN = "vasilver.work@yandex.ru"
PASSWORD = "RainbowClown2"
URL = "https://demowebshop.tricentis.com"


def add_product(product_url, cookie, payload):
    with step("Add product to cart"):
        response = requests.request(
            "POST",
            url="https://demowebshop.tricentis.com/addproducttocart" + product_url,
            data=payload,
            cookies={"NOPCOMMERCE.AUTH": cookie}
        )
        allure.attach(body=response.text, name='Response', attachment_type=AttachmentType.TEXT, extension='.txt')
    return response.status_code


def test_add_products_to_cart():
    cookie = get_cookie()

    with step('Set cookie'):
        browser.open('/')
        browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie})
        browser.open('/')
    with step("Add Laptop to cart via API"):
        resp_code = add_product("/catalog/31/1/1", cookie, None)
        assert resp_code == 200
    with step("Add smartphone to cart via API"):
        resp_code = add_product("/catalog/43/1/1", cookie, None)
        assert resp_code == 200

    browser.element("#topcartlink").click()
    with step("Check products presence in cart"):
        browser.all(".product-name").should(
            have.exact_texts("14.1-inch Laptop", "Smartphone"))
    clear_cart(2)
    browser.element(".page-body").should(have.text("Your Shopping Cart is empty!"))


def test_add_computer_to_cart():
    cookie = get_cookie()

    with step('Set cookie'):
        browser.open('/')
        browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie})
        browser.open('/')

    with step("Add computer to cart via API"):
        resp_code = add_product("/details/74/1", cookie,
                                {'product_attribute_74_5_26': '81', 'product_attribute_74_6_27': '83',
                                 'product_attribute_74_3_28': '86', 'addtocart_74.EnteredQuantity': '1'})
        assert resp_code == 200

    browser.element("#topcartlink").click()
    with step("Check products presence in cart"):
        browser.element(".product-name").should(
            have.exact_text("Build your own expensive computer"))
    clear_cart(1)
    browser.element(".page-body").should(have.text("Your Shopping Cart is empty!"))
