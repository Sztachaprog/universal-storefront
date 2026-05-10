from playwright.sync_api import (
    sync_playwright,
    expect
)
from src.database.database import get_db_connection, close_db_connection
from src.application import(
    get_user_by_id,
    register_user
)

from tests.e2e.pages.register_page import RegisterPage



def test_register(page):

    register_page = RegisterPage(page)
    register_page.navigate()
    register_page.fill_username("testusername")
    register_page.fill_password("testpassword")
    register_page.fill_email("testuser@mail.com")
    register_page.submit()
    
    expect(register_page.success_register()).to_have_text("Succesfully registered")
    