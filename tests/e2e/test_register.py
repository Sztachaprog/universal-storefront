from playwright.sync_api import expect
from src.application import(
    register_user
)
import allure
from tests.e2e.pages.register_page import RegisterPage


@allure.feature("E2E Registration")
def test_correct_register(page):

    register_page = RegisterPage(page)
    register_page.navigate()
    register_page.fill_username("testusername")
    register_page.fill_password("testpassword")
    register_page.fill_email("testuser@mail.com")
    register_page.submit()
    
    expect(register_page.success_register()).to_have_text("Succesfully registered")

@allure.feature("E2E Registration")
def test_too_short_username_register(page):

    register_page = RegisterPage(page)
    register_page.navigate()
    register_page.fill_username("user")
    register_page.fill_password("testpassword")
    register_page.fill_email("testuser@mail.com")
    register_page.submit()
    
    expect(register_page.error_register()).to_have_text("Username is too short")

@allure.feature("E2E Registration")
def test_too_long_username_register(page):

    register_page = RegisterPage(page)
    register_page.navigate()
    register_page.fill_username("u"*31)
    register_page.fill_password("testpassword")
    register_page.fill_email("testuser@mail.com")
    register_page.submit()

    expect(register_page.error_register()).to_have_text("Username is too long")

@allure.feature("E2E Registration")
def test_too_short_password_register(page):

    register_page = RegisterPage(page)
    register_page.navigate()
    register_page.fill_username("testusername")
    register_page.fill_password("passwod")
    register_page.fill_email("testuser@mail.com")
    register_page.submit()
    
    expect(register_page.error_register()).to_have_text("Password is too short")

@allure.feature("E2E Registration")
def test_too_long_password_register(page):

    register_page = RegisterPage(page)
    register_page.navigate()
    register_page.fill_username("testusername")
    register_page.fill_password("p"*75)
    register_page.fill_email("testuser@mail.com")
    register_page.submit()

    expect(register_page.error_register()).to_have_text("Password is too long")

@allure.feature("E2E Registration")
def test_forbidden_characters_in_username_register(page):

    register_page = RegisterPage(page)
    register_page.navigate()
    register_page.fill_username("testusername!")
    register_page.fill_password("testpassword")
    register_page.fill_email("testuser@mail.com")
    register_page.submit()
    
    expect(register_page.error_register()).to_have_text("Forbidden characters in username")

@allure.feature("E2E Registration")
def test_duplicate_username_register(page, registered_user):

    register_page = RegisterPage(page)
    register_page.navigate()
    register_page.fill_username(registered_user.username)
    register_page.fill_password("testpassword")
    register_page.fill_email("testuser2@mail.com")
    register_page.submit()

    expect(register_page.error_register()).to_have_text("Username already exists")

@allure.feature("E2E Registration")
def test_duplicate_email_register(page, registered_user):

    register_page = RegisterPage(page)
    register_page.navigate()
    register_page.fill_username("testusername2")
    register_page.fill_password("testpassword")
    register_page.fill_email(registered_user.email)
    register_page.submit()

    expect(register_page.error_register()).to_have_text("Email already exists")

    