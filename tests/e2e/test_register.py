from playwright.sync_api import (
    sync_playwright,
    expect
)
from src.database.database import get_db_connection, close_db_connection
from src.application import(
    register_user
)


def test_register(page):

    page.goto("http://localhost:5000/register")
    page.fill("input[name='username']", "siema11")
    page.fill("input[name='password']", "siema22")
    page.fill("input[name='email']", "siema1@mail.com")
    page.click("button[type='submit']")
    expect(page.locator("#register-success")).to_be_visible()


def test_login(page):
    

    page.goto("http://localhost:5000/login")
    page.fill("input[name='username']", "siema11")
    page.fill("input[name='password']", "siema22")
    page.click("button[type='submit']")
    expect(page.locator(".welcome-name")).to_have_text("siema11")

