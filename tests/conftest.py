import allure
import pytest
import requests
from allure_commons._allure import step
from allure_commons.types import AttachmentType
from selene import browser

LOGIN = "vasilver.work@yandex.ru"
PASSWORD = "RainbowClown2"
URL = "https://demowebshop.tricentis.com"


@pytest.fixture(autouse=True)
def browser_management():
    browser.config.base_url = URL
    browser.config.window_height = 1080
    browser.config.window_width = 1920

    yield

    browser.quit()


def clear_cart(count):
    for i in range(count):
        browser.element('[name="removefromcart"]').click()
        browser.element(".update-cart-button").click()


def get_cookie():
    with step("Login via API"):
        response = requests.request(
            "POST",
            url=URL + "/login",
            data={"Email": LOGIN, "Password": PASSWORD, "RememberMe": False},
            allow_redirects=False
        )
        cookie = response.cookies.get("NOPCOMMERCE.AUTH")
        allure.attach(body=response.text, name="Response", attachment_type=AttachmentType.TEXT, extension="txt")
        allure.attach(body=cookie, name="Cookie", attachment_type=AttachmentType.TEXT, extension="txt")

    return cookie
