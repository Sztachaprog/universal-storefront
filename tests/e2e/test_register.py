from playwright.sync_api import sync_playwright

def test_register(page):
    page.goto("http://localhost:5000/register")
    page.fill("input[name='username']", "testuser")
    page.fill("input[name='password']", "testpass")
    page.fill("input[name='email']", "test@mail.com")
    page.click("button[type='submit']")

