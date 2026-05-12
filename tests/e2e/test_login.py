from playwright.sync_api import (
    expect
)
from tests.e2e.pages.login_page import LoginPage



def test_correct_login(page, registered_user):

    login_page = LoginPage(page)
    login_page.navigate()
    login_page.fill_username(registered_user.username)
    login_page.fill_password(registered_user.password)
    login_page.submit()
    login_page.get_welcome_name()

    expect(login_page.get_welcome_name()).to_have_text(registered_user.username)

def test_invalid_username_login(page, registered_user):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.fill_username("invalidusername")
    login_page.fill_password(registered_user.password)
    login_page.submit()

    expect(login_page.login_error()).to_have_text("User not found")

def test_invalid_password_login(page, registered_user):

    login_page = LoginPage(page)
    login_page.navigate()
    login_page.fill_username(registered_user.username)
    login_page.fill_password("testpassword1")
    login_page.submit()

    expect(login_page.login_error()).to_have_text("Wrong password")
    