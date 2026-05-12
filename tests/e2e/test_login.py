from playwright.sync_api import (
    expect
)
from src.application import(
    register_user
)
from tests.e2e.pages.login_page import LoginPage


    


def test_login(page, cursor, conn):

    register_user("testusername", "testpassword", "testuser@mail.com", is_premium = False, cursor=cursor)
    conn.commit()
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.fill_username("testusername")
    login_page.fill_password("testpassword")
    login_page.submit()
    login_page.get_welcome_name()

    expect(login_page.get_welcome_name()).to_have_text("testusername")
    